from rest_framework import viewsets, permissions, decorators, response, status
from .models import Doctor, DoctorAvailability
from .serializers import DoctorSerializer, DoctorAvailabilitySerializer
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from hospitals.models import HospitalAdmin, Department, Treatment, Hospital
from django.db import transaction
from django.core.mail import send_mail
from appointments.models import Appointment
from django.utils import timezone
from frontend.decorators import role_required
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth import get_user_model, authenticate, login
from django.contrib.auth.tokens import default_token_generator
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes
from accounts.models import DoctorProfile

User = get_user_model()

@csrf_exempt
def register_doctor(request):
    if request.method == 'POST':
        data = request.POST
        email = data.get('email')
        aadhaar = data.get('aadhaar')
        hospital_id = data.get('hospital')

        # ✅ Check for duplicate email
        if User.objects.filter(email=email).exists():
            return JsonResponse({'status': 'error', 'message': 'Email already exists.'}, status=400)

        # ✅ Check for duplicate Aadhaar
        if DoctorProfile.objects.filter(aadhaar=aadhaar).exists():
            return JsonResponse({'status': 'error', 'message': 'Aadhaar already exists.'}, status=400)

        try:
            with transaction.atomic():
                # Create User without password (unusable)
                user = User.objects.create_user(
                    email=email,
                    password=None, # No password yet
                    phone=data.get('contact_number'),
                    role='doctor',
                    is_active=False 
                )
                user.set_unusable_password()
                user.save()

                DoctorProfile.objects.create(
                    user=user,
                    gender=data.get('gender'),
                    date_of_birth=data.get('date_of_birth'),
                    contact_number=data.get('contact_number'),
                    address=data.get('address'),
                    medical_certificate=request.FILES.get('medical_certificate'),
                    qualification=data.get('qualification'),
                    specialization=data.get('specialization'),
                    year_of_experience=data.get('year_of_experience'),
                    registration_certificate=request.FILES.get('registration_certificate'),
                    degree_certificates=request.FILES.get('degree_certificates'),
                    aadhaar=aadhaar,
                    passport_photo=request.FILES.get('passport_photo'),
                    experience_certificate=request.FILES.get('experience_certificate')
                )

                # Link to Hospital
                hospital = Hospital.objects.get(id=hospital_id)
                Doctor.objects.create(
                    user=user,
                    hospital=hospital,
                    specialization=data.get('specialization'),
                    status=Doctor.STATUS_PENDING
                )

                # Notify Hospital Admin (Optional - could be email)
                # For now, just return success

            return JsonResponse({'status': 'success', 'message': 'Doctor registered. Awaiting hospital approval.'})

        except Exception as e:
            return JsonResponse({'status': 'error', 'message': str(e)}, status=500)

    return JsonResponse({'status': 'error', 'message': 'Invalid request method.'}, status=400)


def doctor_register_page(request):
    hospitals = Hospital.objects.filter(status='approved') # Only show approved hospitals
    return render(request, 'doctors/register.html', {'hospitals': hospitals})


class DoctorAvailabilityViewSet(viewsets.ModelViewSet):
    queryset = DoctorAvailability.objects.all()
    serializer_class = DoctorAvailabilitySerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        if hasattr(user, 'doctor'):
            return DoctorAvailability.objects.filter(doctor=user.doctor)
        return DoctorAvailability.objects.none()

    def perform_create(self, serializer):
        serializer.save(doctor=self.request.user.doctor)


class DoctorViewSet(viewsets.ModelViewSet):
    queryset = Doctor.objects.select_related('hospital', 'department', 'treatment').all()
    serializer_class = DoctorSerializer
    permission_classes = [permissions.IsAuthenticated]

    @decorators.action(detail=True, methods=['post'])
    def approve(self, request, pk=None):
        doctor = self.get_object()
        serializer = self.get_serializer()
        serializer.approve(doctor)
        return response.Response(
            {'status': doctor.status, 'is_verified': doctor.is_verified, 'user_id': doctor.user.id},
            status=status.HTTP_200_OK
        )

    @decorators.action(detail=True, methods=['post'])
    def reject(self, request, pk=None):
        doctor = self.get_object()
        serializer = self.get_serializer()
        serializer.reject(doctor)
        return response.Response(
            {'status': doctor.status, 'is_verified': doctor.is_verified},
            status=status.HTTP_200_OK
        )

    def get_queryset(self):
        qs = super().get_queryset()
        user = self.request.user

        if hasattr(user, 'doctor'):
            return qs.filter(id=user.doctor.id)  # Doctor sees only self
        elif hasattr(user, 'hospital_admin'):
            return qs.filter(hospital=user.hospital_admin.hospital)  # Hospital admin sees own hospital
        elif user.is_superuser:
            return qs  # Super admin sees all
        return qs.none()


class PublicAvailabilityViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = DoctorAvailability.objects.filter(is_available=True)
    serializer_class = DoctorAvailabilitySerializer
    permission_classes = [permissions.AllowAny]


@login_required
@role_required('hospital_admin')
def pending_doctors(request):
    try:
        hospital = HospitalAdmin.objects.get(user=request.user).hospital
    except HospitalAdmin.DoesNotExist:
        messages.error(request, "You are not authorized as a hospital admin.")
        return redirect('homepage') 

    doctors = Doctor.objects.filter(hospital=hospital, status=Doctor.STATUS_PENDING)
    return render(request, 'doctors/pending_doctors.html', {'doctors': doctors})

@login_required
@role_required('hospital_admin')
def approve_doctor(request, doctor_id):
    doctor = get_object_or_404(Doctor, id=doctor_id, hospital__hospitaladmin__user=request.user)
    
    # Generate random password
    password = User.objects.make_random_password()
    user = doctor.user
    user.set_password(password)
    user.is_active = True
    user.save()

    doctor.status = Doctor.STATUS_APPROVED
    doctor.is_approved = True
    doctor.save()

    # Send email with credentials
    login_url = request.build_absolute_uri('/hospital/doctors/login/')
    send_mail(
        subject='Doctor Account Approved',
        message=f'Your account has been approved.\n\nLogin URL: {login_url}\nEmail: {user.email}\nPassword: {password}\n\nPlease change your password after logging in.',
        from_email='blueglobalcloud@gmail.com',
        recipient_list=[user.email],
        fail_silently=False,
    )

    messages.success(request, f'Doctor {doctor.user.email} approved and credentials sent.')
    return redirect('pending_doctors')

# 🏥 Hospital admin dashboard
@login_required
@role_required('hospital_admin')
def hospital_admin_dashboard(request):
    hospital = HospitalAdmin.objects.get(user=request.user).hospital

    departments = Department.objects.filter(hospital=hospital)
    treatments = Treatment.objects.filter(hospital=hospital)
    doctors = Doctor.objects.filter(hospital=hospital)
    appointments = Appointment.objects.filter(
        hospital=hospital,
        appointment_date__gte=timezone.now()
    ).order_by('appointment_date')

    pending_doctors = doctors.filter(status=Doctor.STATUS_PENDING)

    return render(request, 'frontend/hospital_admin/dashboard.html', {
        'hospital': hospital,
        'departments': departments,
        'treatments': treatments,
        'doctors': doctors,
        'appointments': appointments,
        'pending_doctors': pending_doctors,
    })


def doctor_login_view(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
        user = authenticate(request, username=email, password=password)
        if user and user.role == 'doctor':
            login(request, user)
            return redirect('doctor_dashboard')
        else:
            messages.error(request, 'Invalid credentials or not a doctor.')
    return render(request, 'frontend/doctor_login.html')


@login_required
@role_required('doctor')
def doctor_dashboard(request):
    doctor = Doctor.objects.get(user=request.user)

    appointments = Appointment.objects.filter(
        doctor=doctor,
        appointment_date__gte=timezone.now()
    ).order_by('appointment_date')

    availabilities = DoctorAvailability.objects.filter(
        doctor=doctor,
        date__gte=timezone.now().date()
    ).order_by('date', 'start_time')

    return render(request, 'doctor/dashboard.html', {
        'appointments': appointments,
        'availabilities': availabilities
    })
