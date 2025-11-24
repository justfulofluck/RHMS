from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import get_user_model, authenticate, login
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from hospitals.models import Hospital, Treatment, Department, HospitalAdmin
from .decorators import role_required
from accounts.models import DoctorProfile
from appointments.models import Appointment, DoctorAvailability, Doctor
from django.utils import timezone
from django.contrib.auth.forms import AuthenticationForm
from django.core.mail import send_mail
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes
from django.db import transaction, IntegrityError
from django.contrib.auth import login
from django.contrib.admin.views.decorators import staff_member_required
from accounts.views import superadmin_login_ajax

User = get_user_model()

def doctor_login_view(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
        user = authenticate(request, username=email, password=password)
        if user and user.role == 'doctor':
            print("User authenticated successfully.")
            print("User role: ", user.role)
            print("User email: ", user.email)
            print("User is_active: ", user.is_active)
            login(request, user)
            return redirect('doctor_dashboard')
        else:
            messages.error(request, 'Invalid credentials or not a doctor.')
    return render(request, 'frontend/doctor_login.html')


def hospital_login_view(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
        user = authenticate(request, username=email, password=password)
        if user and user.role == 'hospital_admin':
            print("User authenticated successfully.")
            print("User role: ", user.role)
            print("User email: ", user.email)
            print("User is_active: ", user.is_active)
            login(request, user)
            return redirect('hospital_admin_dashboard')
        else:
            messages.error(request, 'Invalid credentials or not a hospital admin.')
    return render(request, 'frontend/hospital_login.html')


# 🏥 Hospital registration page
def hospital_register_page(request):
    return render(request, 'frontend/hospital_admin/register.html')


# 🏥 AJAX hospital registration with FormData support
@csrf_exempt
def register_hospital_ajax(request):
    if request.method == 'POST':
        try:
            with transaction.atomic():
                # Step 1 - Create user with pending status
                user = User.objects.create_user(
                    email=request.POST.get('email'),
                    password=request.POST.get('password'),
                    phone=request.POST.get('phone_number'),
                    role='pending_hospital_admin',  # ✅ Assign pending role
                    is_active=True
                )

                # Step 2 - Create hospital with pending status
                hospital = Hospital.objects.create(
                    name=request.POST.get('name'),
                    registration_number=request.POST.get('registration_number'),
                    email=request.POST.get('email'),
                    phone_number=request.POST.get('phone_number'),
                    address=request.POST.get('address'),
                    city=request.POST.get('city'),
                    state=request.POST.get('state', 'Gujarat'),
                    country=request.POST.get('country', 'India'),
                    hospital_type=request.POST.get('hospital_type', 'general'),
                    hours=request.POST.get('hours', '9:00 AM - 5:00 PM'),
                    logo=request.FILES.get('logo'),
                    status=Hospital.STATUS_PENDING
                )

                # Step 3: Link hospital admin profile
                HospitalAdmin.objects.create(user=user, hospital=hospital)

                # ✅ Send confirmation email
                send_mail(
                    subject='Hospital Registration Submitted',
                    message='A new hospital has been registered. Admin will review and approve it.',
                    from_email='blueglobalcloud@gmail.com',
                    recipient_list=[hospital.email],
                    fail_silently=False,
                )
            
            return JsonResponse({'status': 'success', 'message': 'Hospital registration submitted. Awaiting approval.'})
        except IntegrityError:
            return JsonResponse({'status': 'error', 'message': 'A hospital with this email or registration number already exists.'}, status=400)
        except Exception as e:
            return JsonResponse({'status': 'error', 'message': str(e)}, status=500)

    return JsonResponse({'status': 'error', 'message': 'Invalid request method.'}, status=400)

# 👨‍⚕️ Doctor registration via AJAX
@csrf_exempt
def register_doctor_ajax(request):
    if request.method == 'POST':
        data = request.POST
        email = data.get('email')
        aadhaar = data.get('aadhaar')

        # ✅ Check for duplicate email
        if User.objects.filter(email=email).exists():
            return JsonResponse({'status': 'error', 'message': 'Email already exists.'}, status=400)

        # ✅ Check for duplicate Aadhaar
        if DoctorProfile.objects.filter(aadhaar=aadhaar).exists():
            return JsonResponse({'status': 'error', 'message': 'Aadhaar already exists.'}, status=400)

        try:
            user = User.objects.create_user(
                email=email,
                password=data.get('password'),
                phone=data.get('contact_number'),
                role='doctor',
                is_active=False  # 🔐 Inactive until email confirmation
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

            # ✅ Send activation email
            token = default_token_generator.make_token(user)
            uid = urlsafe_base64_encode(force_bytes(user.pk))
            activation_link = f"http://192.168.1.208:8000/activate-doctor/?uid={uid}&token={token}"

            send_mail(
                subject="Activate Your Doctor Account",
                message=f"Click the link to activate your account: {activation_link}",
                from_email=None,
                recipient_list=[email],
            )

            return JsonResponse({'status': 'success', 'message': 'Doctor registered. Please check your email to activate your account.'})

        except Exception as e:
            return JsonResponse({'status': 'error', 'message': str(e)}, status=500)

    return JsonResponse({'status': 'error', 'message': 'Invalid request method.'}, status=400)


# 🏥 Hospital admin dashboard
@login_required
@role_required('hospital_admin', 'superadmin')
def hospital_admin_dashboard(request):
    try:
        hospital_admin = HospitalAdmin.objects.get(user=request.user)
        hospital = hospital_admin.hospital
    except HospitalAdmin.DoesNotExist:
        messages.error(request, "Hospital admin record not found.")
        return redirect('hospital_login')

    departments = Department.objects.filter(hospital=hospital)
    treatments = Treatment.objects.filter(hospital=hospital)
    doctors = Doctor.objects.filter(hospital=hospital)
    appointments = Appointment.objects.filter(
        hospital=hospital,
        appointment_date__gte=timezone.now()
    ).order_by('appointment_date')

    return render(request, 'frontend/hospital_admin/dashboard.html', {
        'hospital': hospital,
        'departments': departments,
        'treatments': treatments,
        'doctors': doctors,
        'appointments': appointments
    })


# 👨‍⚕️ Doctor dashboard
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


# 🔐 Password reset confirmation page
def reset_password_confirm_page(request):
    uid = request.GET.get('uid')
    token = request.GET.get('token')
    return render(request, 'frontend/reset_password_confirm.html', {'uid': uid, 'token': token})


# 🔐 Password reset request page
def request_password_reset_page(request):
    return render(request, 'frontend/request_password_reset.html')


def doctor_register_page(request):
    return render(request, 'frontend/doctor/register.html')


