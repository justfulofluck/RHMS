from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
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
                    role='pending_hospital_admin',
                    is_active=True  # ✅ Set inactive until approved
                )

                # Step 2 - Collect hospital types (checkboxes)
                hospital_types = request.POST.getlist('type')  # e.g., ['General', 'Pediatric']

                # Step 3 - Collect operating hours
                days = ["monday", "tuesday", "wednesday", "thursday", "friday", "saturday", "sunday"]
                hours = {}
                for day in days:
                    open_time = request.POST.get(f"{day}_open", "")
                    close_time = request.POST.get(f"{day}_close", "")
                    hours[day.capitalize()] = f"{open_time}-{close_time}" if open_time and close_time else "Closed"

                # Step 4 - Create hospital
                hospital = Hospital.objects.create(
                    name=request.POST.get('name'),
                    registration_number=request.POST.get('registration_number'),
                    email=request.POST.get('email'),
                    phone_number=request.POST.get('phone_number'),
                    address=request.POST.get('address'),
                    city=request.POST.get('city'),
                    state=request.POST.get('state', 'Gujarat'),
                    country=request.POST.get('country', 'India'),
                    hospital_type=hospital_types,
                    hours=hours,
                    logo=request.FILES.get('logo'),
                    status=Hospital.STATUS_PENDING
                )

                # Step 5 - Link hospital admin profile
                HospitalAdmin.objects.create(user=user, hospital=hospital)

                # Step 6 - Send confirmation email
                send_mail(
                    subject='Hospital Registration Submitted',
                    message='A new hospital has been registered. Admin will review and approve it.',
                    from_email='blueglobalcloud@gmail.com',
                    recipient_list=[hospital.email],
                    fail_silently=False,
                )

            return JsonResponse({
                'status': 'success',
                'message': 'Hospital registration submitted. Awaiting approval.'
            })

        except IntegrityError:
            return JsonResponse({
                'status': 'error',
                'message': 'A hospital with this email or registration number already exists.'
            }, status=400)

        except Exception as e:
            return JsonResponse({
                'status': 'error',
                'message': str(e)
            }, status=500)

    return JsonResponse({
        'status': 'error',
        'message': 'Invalid request method.'
    }, status=400)



# 👨‍⚕️ Doctor registration via AJAX




@login_required
@role_required('hospital_admin')
def edit_hospital_admin(request):
    hospital = HospitalAdmin.objects.get(user=request.user).hospital

    if request.method == 'POST':
        hospital.name = request.POST.get('name')
        hospital.phone_number = request.POST.get('phone_number')
        hospital.address = request.POST.get('address')
        hospital.city = request.POST.get('city')
        hospital.state = request.POST.get('state')
        hospital.country = request.POST.get('country')
        hospital.hospital_type = request.POST.get('hospital_type')

        # Update Hours
        days = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
        hours = {}
        for day in days:
            open_time = request.POST.get(f"{day.lower()}_open_time")
            close_time = request.POST.get(f"{day.lower()}_close_time")
            hours[day] = f"{open_time}-{close_time}" if open_time and close_time else "Closed"
        hospital.hours = hours

        if request.FILES.get('logo'):
            hospital.logo = request.FILES.get('logo')

        hospital.save()
        messages.success(request, 'Hospital updated successfully.')
        return redirect('hospital_admin_dashboard')

    return render(request, 'frontend/hospital_admin/edit_hospital.html', {'hospital': hospital})




# 🔐 Password reset confirmation page
def reset_password_confirm_page(request):
    uid = request.GET.get('uid')
    token = request.GET.get('token')
    return render(request, 'frontend/reset_password_confirm.html', {'uid': uid, 'token': token})


# 🔐 Password reset request page
def request_password_reset_page(request):
    return render(request, 'frontend/request_password_reset.html')




def hospital_register_page(request):
    days = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
    return render(request, 'frontend/hospital_admin/register.html', {'days': days})


from django.contrib.auth.decorators import user_passes_test
from accounts.views import is_superadmin

@user_passes_test(is_superadmin)
def approve_hospital(request, hospital_id):
    hospital = get_object_or_404(Hospital, id=hospital_id)
    hospital.status = Hospital.STATUS_APPROVED
    hospital.is_approved = True
    hospital.save()

    # Activate the hospital admin user
    # Use filter().first() to handle cases with 0 or >1 admins safely
    admin = HospitalAdmin.objects.filter(hospital=hospital).first()
    
    if admin:
        if admin.user:
            # Generate a random password
            from django.utils.crypto import get_random_string
            password = get_random_string(length=10)
            admin.user.set_password(password)
            admin.user.is_active = True
            admin.user.role = 'hospital_admin'  # Update role from pending_hospital_admin
            admin.user.save()
            
            # Send approval email with credentials
            login_url = request.build_absolute_uri(reverse('hospital_login'))
            try:
                send_mail(
                    subject='Hospital Registration Approved - Login Credentials',
                    message=f'Your hospital registration has been approved.\n\n'
                            f'Here are your login credentials:\n'
                            f'Email: {hospital.email}\n'
                            f'Password: {password}\n\n'
                            f'Login here: {login_url}',
                    from_email='blueglobalcloud@gmail.com',
                    recipient_list=[hospital.email],
                    fail_silently=False,
                )
            except Exception as e:
                messages.warning(request, f'Hospital approved, but failed to send email: {e}')
        else:
             messages.warning(request, f'Hospital {hospital.name} approved, but admin user is missing.')
        
        messages.success(request, f'Hospital {hospital.name} approved successfully.')
    else:
        messages.warning(request, f'Hospital {hospital.name} approved, but no admin user found.')

    return redirect('superadmin_dashboard')

def homepage(request):
    return render(request, 'frontend/homepage.html')

def appointment_widget(request):
    return render(request, 'frontend/appointment_widget.html')