from rest_framework import viewsets, permissions, decorators, response, status
from .models import Doctor, DoctorAvailability
from .serializers import DoctorSerializer, DoctorAvailabilitySerializer
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
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
from django.utils.crypto import get_random_string
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


        try:
            with transaction.atomic():
                # Generate random password for doctor
                password = get_random_string(length=12)
                
                # Create User with password and active status
                user = User.objects.create_user(
                    email=email,
                    password=password,  # ✅ Generated password
                    phone=data.get('contact_number'),
                    role='doctor',  # ✅ Active role
                    is_active=True  # ✅ Can login immediately
                )

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
                    name=data.get('name'),
                    hospital=hospital,
                    specialization=data.get('specialization'),
                    status=Doctor.STATUS_PENDING  # ✅ Pending until hospital admin approves
                )

                # Send registration email with login credentials
                login_url = request.build_absolute_uri(reverse('doctor_login'))
                send_mail(
                    subject='Doctor Registration - Login Credentials',
                    message=f'Welcome to RHMS!\n\n'
                            f'Your doctor account has been registered successfully.\n\n'
                            f'Login Credentials:\n'
                            f'Email: {user.email}\n'
                            f'Password: {password}\n\n'
                            f'Login URL: {login_url}\n\n'
                            f'IMPORTANT: Your profile is currently in DRAFT MODE.\n'
                            f'You can login and set your availability, but you will be visible '
                            f'to patients only after hospital admin approval.\n\n'
                            f'Please complete your profile and wait for approval.\n\n'
                            f'Thank you for joining RHMS!',
                    from_email='blueglobalcloud@gmail.com',
                    recipient_list=[user.email],
                    fail_silently=False,
                )

            messages.success(request, 'Registration successful! Check your email for login credentials.')
            return redirect('doctor_login')

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
        else:
            # ✅ Regular users (patients) only see approved doctors from approved hospitals
            return qs.filter(
                hospital__status=Hospital.STATUS_APPROVED,
                status=Doctor.STATUS_APPROVED
            )
        return qs.none()


class PublicAvailabilityViewSet(viewsets.ReadOnlyModelViewSet):
    # ✅ Only show availability for doctors from approved hospitals
    # Note: doctor field points to User, User.doctor points to Doctor model
    queryset = DoctorAvailability.objects.filter(
        is_available=True,
        doctor__doctor__hospital__status=Hospital.STATUS_APPROVED
    )
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

    # Get all doctors for this hospital
    all_doctors = Doctor.objects.filter(hospital=hospital).select_related('user', 'department', 'user__doctorprofile')
    pending_doctors_list = all_doctors.filter(status=Doctor.STATUS_PENDING)
    
    return render(request, 'doctors/pending_doctors.html', {
        'hospital': hospital,
        'all_doctors': all_doctors,
        'pending_doctors': pending_doctors_list,
    })

@login_required
@role_required('hospital_admin')
def approve_doctor(request, doctor_id):
    doctor = get_object_or_404(Doctor, id=doctor_id, hospital__hospitaladmin__user=request.user)
    
    # User already has credentials from registration
    # Just ensure user is active (should already be active)
    user = doctor.user
    user.is_active = True
    user.save()

    doctor.status = Doctor.STATUS_APPROVED
    doctor.is_approved = True
    doctor.save()

    # Send approval notification email (no credentials needed)
    hospital = doctor.hospital
    send_mail(
        subject='Doctor Account Approved - Now Live!',
        message=f'Congratulations!\n\n'
                f'Your doctor account has been approved by {hospital.name}.\n\n'
                f'Your profile is now LIVE and visible to patients.\n'
                f'Patients can now:\n'
                f'- Find you in doctor search\n'
                f'- View your availability\n'
                f'- Book appointments with you\n\n'
                f'You can continue managing your availability through the dashboard.\n\n'
                f'Thank you for joining RHMS!',
        from_email='blueglobalcloud@gmail.com',
        recipient_list=[user.email],
        fail_silently=False,
    )

    messages.success(request, f'Doctor {doctor.user.email} approved successfully.')
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
    hospital = doctor.hospital
    
    # Get today's date
    today = timezone.now().date()
    
    # All upcoming appointments
    appointments = Appointment.objects.filter(
        doctor=doctor,
        appointment_date__gte=timezone.now()
    ).order_by('appointment_date')
    
    # Today's appointments count
    today_appointments = Appointment.objects.filter(
        doctor=doctor,
        appointment_date__date=today
    ).count()
    
    # Total unique patients (based on patient_name)
    total_patients = Appointment.objects.filter(
        doctor=doctor
    ).values('patient_name').distinct().count()
    
    # Availabilities
    availabilities = DoctorAvailability.objects.filter(
        doctor=doctor.user,
        date__gte=today
    ).order_by('date', 'start_time')
    
    return render(request, 'doctors/dashboard.html', {
        'doctor': doctor,
        'hospital': hospital,
        'appointments': appointments,
        'today_appointments': today_appointments,
        'total_patients': total_patients,
        'reports_count': 0,  # Placeholder for future feature
        'availabilities': availabilities
    })


@login_required
@role_required('hospital_admin')
def edit_doctor(request, doctor_id):
    """Edit doctor information - only accessible by hospital admin"""
    try:
        hospital = HospitalAdmin.objects.get(user=request.user).hospital
    except HospitalAdmin.DoesNotExist:
        messages.error(request, "You are not authorized as a hospital admin.")
        return redirect('homepage')
    
    # Get doctor and ensure they belong to this hospital
    doctor = get_object_or_404(Doctor, id=doctor_id, hospital=hospital)
    
    if request.method == 'POST':
        try:
            with transaction.atomic():
                # Update Doctor model
                doctor.name = request.POST.get('name')
                doctor.specialization = request.POST.get('specialization')
                
                # Update department if provided
                department_id = request.POST.get('department')
                if department_id:
                    doctor.department = Department.objects.get(id=department_id)
                else:
                    doctor.department = None
                
                # Update treatments
                doctor.treatments.clear()
                treatment_ids = request.POST.getlist('treatments')
                for treatment_id in treatment_ids:
                    treatment = Treatment.objects.get(id=treatment_id)
                    doctor.treatments.add(treatment)
                
                doctor.save()
                
                # Update DoctorProfile if exists
                if hasattr(doctor.user, 'doctorprofile'):
                    profile = doctor.user.doctorprofile
                    profile.contact_number = request.POST.get('contact_number', profile.contact_number)
                    profile.gender = request.POST.get('gender', profile.gender)
                    
                    dob = request.POST.get('date_of_birth')
                    if dob:
                        profile.date_of_birth = dob
                    
                    profile.qualification = request.POST.get('qualification', profile.qualification)
                    profile.year_of_experience = request.POST.get('year_of_experience', profile.year_of_experience)
                    profile.address = request.POST.get('address', profile.address)
                    profile.save()
                
                # Update User phone
                phone = request.POST.get('contact_number')
                if phone:
                    doctor.user.phone = phone
                    doctor.user.save()
                
                messages.success(request, f'Doctor {doctor.name} updated successfully.')
                return redirect('hospital_admin_dashboard')
                
        except Exception as e:
            messages.error(request, f'Error updating doctor: {str(e)}')
    
    # Get departments and treatments for this hospital
    departments = Department.objects.filter(hospital=hospital)
    treatments = Treatment.objects.filter(hospital=hospital)
    treatment_ids = list(doctor.treatments.values_list('id', flat=True))
    
    return render(request, 'doctors/edit_doctor.html', {
        'doctor': doctor,
        'departments': departments,
        'treatments': treatments,
        'treatment_ids': treatment_ids,
    })


@csrf_exempt
@login_required
@role_required('doctor')
def update_appointment_status(request, appointment_id):
    """Update appointment status (Completed, No Show, etc.)"""
    if request.method == 'POST':
        try:
            doctor = Doctor.objects.get(user=request.user)
            appointment = get_object_or_404(Appointment, id=appointment_id, doctor=doctor)
            
            new_status = request.POST.get('status')
            if new_status in ['completed', 'no_show', 'cancelled']:
                appointment.status = new_status
                if new_status == 'cancelled':
                    appointment.cancelled_at = timezone.now()
                    appointment.cancellation_reason = "Cancelled by doctor"
                appointment.save()
                return JsonResponse({'success': True, 'status': new_status})
            else:
                return JsonResponse({'error': 'Invalid status'}, status=400)
                
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)
            
    return JsonResponse({'error': 'Invalid request method'}, status=405)


@login_required
@role_required('doctor')
def my_patients_view(request):
    """List patients who have booked appointments with this doctor"""
    doctor = Doctor.objects.get(user=request.user)
    
    # Aggregate patients based on name (since we don't have a direct Patient FK in Appointment currently)
    # We want: Name, Last Visit, Total Visits
    from django.db.models import Count, Max
    
    patients = Appointment.objects.filter(doctor=doctor).values('patient_name').annotate(
        total_visits=Count('id'),
        last_visit=Max('appointment_date')
    ).order_by('-last_visit')
    
    return render(request, 'doctors/my_patients.html', {
        'doctor': doctor,
        'patients': patients
    })


@login_required
@role_required('doctor')
def edit_my_profile(request):
    """Allow doctors to edit their own profile"""
    doctor = Doctor.objects.get(user=request.user)
    
    if request.method == 'POST':
        try:
            with transaction.atomic():
                # Doctors can update their own: Name, Specialization
                doctor.name = request.POST.get('name', doctor.name)
                doctor.specialization = request.POST.get('specialization', doctor.specialization)
                doctor.save()

                # Profile Details
                if hasattr(doctor.user, 'doctorprofile'):
                    profile = doctor.user.doctorprofile
                    profile.contact_number = request.POST.get('contact_number', profile.contact_number)
                    profile.gender = request.POST.get('gender', profile.gender)
                    profile.qualification = request.POST.get('qualification', profile.qualification)
                    profile.year_of_experience = request.POST.get('year_of_experience', profile.year_of_experience)
                    profile.address = request.POST.get('address', profile.address)
                    
                    dob = request.POST.get('date_of_birth')
                    if dob:
                        profile.date_of_birth = dob
                    
                    profile.save()

                # User Phone
                phone = request.POST.get('contact_number')
                if phone:
                    doctor.user.phone = phone
                    doctor.user.save()
                
                # Update Treatments
                treatment_ids = request.POST.getlist('treatments')
                if treatment_ids:
                    doctor.treatments.clear()
                    for t_id in treatment_ids:
                        doctor.treatments.add(t_id)
            
            return JsonResponse({'success': True, 'message': 'Profile updated successfully.'})

        except Exception as e:
            return JsonResponse({'success': False, 'error': str(e)})

    # GET Request
    # Reuse edit_doctor.html but we need to pass context similar to what it expects
    departments = Department.objects.filter(hospital=doctor.hospital)
    treatments = Treatment.objects.filter(hospital=doctor.hospital)
    treatment_ids_list = list(doctor.treatments.values_list('id', flat=True))
    treatment_ids = ", ".join(map(str, treatment_ids_list))

    return render(request, 'doctors/edit_doctor.html', {
        'doctor': doctor,
        'departments': departments, # Passed but maybe read-only in logic?
        'treatments': treatments,
        'treatment_ids': treatment_ids
    })
