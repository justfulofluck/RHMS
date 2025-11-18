from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import get_user_model, authenticate, login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from hospitals.models import Hospital, Treatment, Department
from accounts.forms.hospital_admin import HospitalAdminRegistrationForm, DoctorRegistrationForm
from .decorators import role_required
from accounts.models import DoctorProfile
from appointments.models import Appointment, DoctorAvailability, Doctor
from django.utils import timezone
from django.contrib.auth.forms import AuthenticationForm

User = get_user_model()

# 🔐 Login view using raw POST
def login_view(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
        user = authenticate(request, username=email, password=password)
        if user is not None:
            login(request, user)
            if user.role == 'hospital_admin':
                return redirect('hospital_admin_dashboard')
            elif user.role == 'doctor':
                return redirect('doctor_dashboard')
            else:
                messages.error(request, "Unknown role.")
        else:
            messages.error(request, 'Invalid credentials')
    return render(request, 'frontend/login.html')


# 🔐 Login view using Django's AuthenticationForm
def user_login(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            if user.role == 'hospital_admin':
                return redirect('hospital_admin_dashboard')
            elif user.role == 'doctor':
                return redirect('doctor_dashboard')
            else:
                messages.error(request, "Unknown role.")
        else:
            messages.error(request, "Invalid credentials.")
    else:
        form = AuthenticationForm()

    return render(request, 'frontend/login.html', {'form': form})

# 🏥 Hospital registration page
def hospital_register_page(request):
    return render(request, 'frontend/hospital_admin/register.html')

# 🏥 AJAX hospital registration with FormData support
@csrf_exempt
def register_hospital_ajax(request):
    if request.method == 'POST':
        try:
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
            return JsonResponse({'status': 'success', 'message': 'Hospital registration submitted. Awaiting approval.'})
        except Exception as e:
            return JsonResponse({'status': 'error', 'message': str(e)}, status=500)

    return JsonResponse({'status': 'error', 'message': 'Invalid request method.'}, status=400)

# 👨‍⚕️ Doctor registration
def register_doctor(request):
    if request.method == 'POST':
        form = DoctorRegistrationForm(request.POST, request.FILES)
        if form.is_valid():
            data = form.cleaned_data

            user = User.objects.create_user(
                email=data['email'],
                password=data['password'],
                phone=data['contact_number'],
                role='doctor'
            )

            DoctorProfile.objects.create(
                user=user,
                gender=data['gender'],
                date_of_birth=data['date_of_birth'],
                contact_number=data['contact_number'],
                address=data['address'],
                registration_number=data['registration_number'],
                medical_certificate=data['medical_certificate'],
                qualification=data['qualification'],
                specialization=data['specialization'],
                year_of_experience=data['year_of_experience'],
                designation=data['designation'],
                department=data['department'],
                timing=data['timing'],
                opd_timings=data['opd_timings'],
                availability_status=data['availability_status'],
                registration_certificate=data['registration_certificate'],
                degree_certificates=data['degree_certificates'],
                aadhaar=data['aadhaar'],
                passport_photo=data['passport_photo'],
                experience_certificate=data.get('experience_certificate')
            )

            messages.success(request, "Doctor registered successfully.")
            return redirect('login')
        else:
            messages.error(request, "Please correct the errors below.")
    else:
        form = DoctorRegistrationForm()

    return render(request, 'doctor/register.html', {'form': form})

# 🏥 Hospital admin dashboard
@login_required
@role_required('hospital_admin', 'superadmin')
def hospital_admin_dashboard(request):
    hospital = Hospital.objects.get(user=request.user)

    departments = Department.objects.filter(hospital=hospital)
    treatments = Treatment.objects.filter(hospital=hospital)
    doctors = Doctor.objects.filter(hospital=hospital)
    appointments = Appointment.objects.filter(
        hospital=hospital,
        appointment_date__gte=timezone.now()
    ).order_by('appointment_date')

    return render(request, 'hospital_admin/dashboard.html', {
        'hospital': hospital,
        'departments': departments,
        'treatments': treatments,
        'doctors': doctors,
        'appointments': appointments
    })

# 👨‍⚕️ Doctor dashboard
@role_required('doctor')
@login_required
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
