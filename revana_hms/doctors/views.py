from rest_framework import viewsets, permissions, decorators, response, status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
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
from patients.models import Patient
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


@login_required
@role_required('hospital_admin')
def add_doctor_page(request):
    """Page for hospital admin to add a new doctor"""
    try:
        hospital_admin = HospitalAdmin.objects.get(user=request.user)
        hospital = hospital_admin.hospital
    except HospitalAdmin.DoesNotExist:
        messages.error(request, "You are not authorized as a hospital admin.")
        return redirect('homepage')
        
    return render(request, 'doctors/add_doctor.html', {'hospital': hospital})


@csrf_exempt
@login_required
@role_required('hospital_admin')
def add_doctor_submit(request):
    """Handle submission of new doctor by hospital admin"""
    if request.method == 'POST':
        try:
            hospital_admin = HospitalAdmin.objects.get(user=request.user)
            hospital = hospital_admin.hospital
        except HospitalAdmin.DoesNotExist:
            return JsonResponse({'status': 'error', 'message': 'Unauthorized'}, status=403)
            
        data = request.POST
        email = data.get('email')
        aadhaar = data.get('aadhaar')
        
        # Verify hospital ID matches (security check)
        form_hospital_id = data.get('hospital')
        if str(hospital.id) != str(form_hospital_id):
             return JsonResponse({'status': 'error', 'message': 'Hospital mismatch'}, status=400)

        # Check for duplicate email
        if User.objects.filter(email=email).exists():
            messages.error(request, 'Email already exists.')
            return redirect('add_doctor_page')

        try:
            with transaction.atomic():
                # Generate random password for doctor
                password = get_random_string(length=12)
                
                # Create User with password and active status
                user = User.objects.create_user(
                    email=email,
                    password=password,
                    phone=data.get('contact_number'),
                    role='doctor',
                    is_active=True
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

                # Link to Hospital & Auto-Approve
                Doctor.objects.create(
                    user=user,
                    name=data.get('name'),
                    hospital=hospital,
                    specialization=data.get('specialization'),
                    status=Doctor.STATUS_APPROVED,  # Auto-approved since admin added
                    is_approved=True
                )

                # Send registration email with login credentials
                login_url = request.build_absolute_uri(reverse('doctor_login'))
                send_mail(
                    subject='Doctor Account Created - Login Credentials',
                    message=f'Welcome to RHMS!\n\n'
                            f'Your doctor account has been created by {hospital.name}.\n\n'
                            f'Login Credentials:\n'
                            f'Email: {user.email}\n'
                            f'Password: {password}\n\n'
                            f'Login URL: {login_url}\n\n'
                            f'Your account is ACTIVE and ready to use.\n'
                            f'Please login to update your availability.\n\n'
                            f'Thank you for joining RHMS!',
                    from_email='blueglobalcloud@gmail.com',
                    recipient_list=[user.email],
                    fail_silently=False,
                )

            messages.success(request, f'Doctor {data.get("name")} added successfully.')
            return redirect('pending_doctors') # Or back to dashboard

        except Exception as e:
            messages.error(request, f'Error adding doctor: {str(e)}')
            return redirect('add_doctor_page')

    return redirect('add_doctor_page')



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
    queryset = Doctor.objects.select_related('hospital', 'department').prefetch_related('treatments').all()
    serializer_class = DoctorSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

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

        # Handle hospital_id filter from query parameters
        hospital_id = self.request.query_params.get('hospital_id')
        if hospital_id:
            qs = qs.filter(hospital_id=hospital_id)

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
    today = timezone.localdate()
    appointments = Appointment.objects.filter(
        hospital=hospital,
        appointment_date__date__gte=today
    ).order_by('appointment_date')

    # Dashboard Stats
    total_departments = departments.count()
    total_doctors = doctors.count()
    total_treatments = treatments.count()
    # Estimate total patients (distinct emails in appointments)
    total_patients = Appointment.objects.filter(hospital=hospital).values('patient_email').distinct().count()

    # Today's Appointments for Table
    today = timezone.localdate()
    todays_appointments = Appointment.objects.filter(
        hospital=hospital,
        appointment_date__date=today
    ).order_by('appointment_date')

    pending_doctors = doctors.filter(status=Doctor.STATUS_PENDING)

    import json
    from django.core.serializers.json import DjangoJSONEncoder

    # Serialize appointments for the calendar widget
    appointments_list = []
    for appt in appointments:
        appointments_list.append({
            'id': appt.id,
            'patient_name': appt.patient_name,
            'doctor_name': appt.doctor.name if appt.doctor else "Unknown",
            'date': appt.appointment_date.strftime('%Y-%m-%d'),
            'time': appt.appointment_date.strftime('%I:%M %p'),
            'status': appt.status,
            'type': "General Visit", # Placeholder as 'type' isn't in model yet
            'doctor_image': appt.doctor.user.doctorprofile.passport_photo.url if hasattr(appt.doctor.user, 'doctorprofile') and appt.doctor.user.doctorprofile.passport_photo else None
        })
    
    appointments_json = json.dumps(appointments_list, cls=DjangoJSONEncoder)

    return render(request, 'frontend/hospital_admin/dashboard.html', {
        'hospital': hospital,
        'departments': departments,
        'treatments': treatments,
        'doctors': doctors,
        'appointments': appointments,
        'todays_appointments': todays_appointments,
        'total_departments': total_departments,
        'total_doctors': total_doctors,
        'total_treatments': total_treatments,
        'total_patients': total_patients,
        'appointments_json': appointments_json,
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
    
    today = timezone.localdate()
    
    # Get Queue Status
    from appointments.models import DailyQueue
    queue, _ = DailyQueue.objects.get_or_create(doctor=doctor, date=today)
    current_token = queue.current_token

    # ✅ Today's Appointments (Waiting List Only)
    # Exclude Completed/Cancelled AND Current Serving
    # We evaluate to a list to allow attribute assignment
    appointments_today_qs = Appointment.objects.filter(
        doctor=doctor,
        appointment_date__date=today,
        status__in=['scheduled', 'confirmed']
    ).exclude(token_number=current_token).order_by('appointment_date')
    
    appointments_today = []
    for appt in appointments_today_qs:
        # Check for history
        if appt.patient_email:
            has_history = Appointment.objects.filter(
                doctor=doctor,
                patient_email__iexact=appt.patient_email,
                status='completed'
            ).exclude(id=appt.id).exists()
        else:
            has_history = Appointment.objects.filter(
                doctor=doctor,
                patient_name__iexact=appt.patient_name,
                status='completed'
            ).exclude(id=appt.id).exists()
        
        # Get Patient Phone
        appt.patient_phone = ""
        if appt.patient_email:
            try:
                patient_obj = Patient.objects.filter(user__email=appt.patient_email).first()
                if patient_obj:
                    appt.patient_phone = patient_obj.phone
            except Exception:
                pass
        
        # Fallback: Try by Name if phone is still empty
        if not appt.patient_phone and appt.patient_name:
            try:
                # Try finding by Patient Name
                patient_obj = Patient.objects.filter(name__iexact=appt.patient_name).first()
                if patient_obj:
                     appt.patient_phone = patient_obj.phone
                else:
                     # Try finding by User Username (if name is actually a username)
                     patient_obj = Patient.objects.filter(user__username__iexact=appt.patient_name).first()
                     if patient_obj:
                         appt.patient_phone = patient_obj.phone
            except Exception:
                pass

        appt.has_history = has_history
        appt.visit_status = "Returning" if has_history else "New" # Also populate for badge
        appointments_today.append(appt)

    
    # Today's appointments count (Total for the day, not just waiting)
    today_appointments_count = Appointment.objects.filter(
        doctor=doctor,
        appointment_date__date=today
    ).count()
    
    # Total unique patients (based on patient_name)
    total_patients = Appointment.objects.filter(
        doctor=doctor
    ).values('patient_name').distinct().count()
    
    # All upcoming appointments (restored)
    upcoming_appointments = Appointment.objects.filter(
        doctor=doctor,
        appointment_date__gte=timezone.now()
    ).order_by('appointment_date')
    
    # Availabilities
    availabilities = DoctorAvailability.objects.filter(
        doctor=doctor.user,
        date__gte=today
    ).order_by('date', 'start_time')
    
    return render(request, 'doctors/dashboard.html', {
        'doctor': doctor,
        'hospital': hospital,
        'appointments': appointments_today, # ✅ Now a list with annotated attributes
        'upcoming_appointments': upcoming_appointments, 
        'today_appointments': today_appointments_count,
        'total_patients': total_patients,
        'reports_count': 0,  
        'availabilities': availabilities
    })


@login_required
@role_required('hospital_admin')
def edit_doctor(request, doctor_id):
    """Edit doctor information - accessible by hospital admin and superuser"""
    
    if request.user.is_superuser:
        # Superuser can edit any doctor
        doctor = get_object_or_404(Doctor, id=doctor_id)
        hospital = doctor.hospital
    else:
        # Hospital Admin can only edit doctors in their hospital
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
    
    # Aggregate patients based on name
    from django.db.models import Count, Max, Q
    from django.utils import timezone
    import hashlib
    import random
    
    # Filtering Logic
    start_date = request.GET.get('start_date')
    end_date = request.GET.get('end_date')
    search_query = request.GET.get('search')
    
    query = Q(doctor=doctor)
    if start_date:
        query &= Q(appointment_date__date__gte=start_date)
    if end_date:
        query &= Q(appointment_date__date__lte=end_date)
    if search_query:
        query &= Q(patient_name__icontains=search_query)
        
    all_patients_qs = Appointment.objects.filter(query).values('patient_name').annotate(
        total_visits=Count('id'),
        last_visit=Max('appointment_date')
    ).order_by('-last_visit')

    # Handle Export CSV
    if request.GET.get('export') == 'csv':
        import csv
        from django.http import HttpResponse
        
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = f'attachment; filename="patients_{timezone.now().strftime("%Y%m%d")}.csv"'
        
        writer = csv.writer(response)
        writer.writerow(['Patient Name', 'Last Visit', 'Total Visits', 'Pseudo ID'])
        
        for p in all_patients_qs:
            pseudo_id = f"PT-{int(hashlib.md5(p['patient_name'].encode()).hexdigest(), 16) % 10000:04d}"
            writer.writerow([
                p['patient_name'], 
                p['last_visit'].strftime('%Y-%m-%d %H:%M'), 
                p['total_visits'],
                pseudo_id
            ])
        return response

    # Total unique patients count for stats
    total_active = all_patients_qs.count()

    # Pagination Logic
    from django.core.paginator import Paginator
    paginator = Paginator(all_patients_qs, 5) # Show 5 patients per page
    page_number = request.GET.get('page')
    patients_page = paginator.get_page(page_number)
    
    # Simple growth calculation
    thirty_days_ago = timezone.now() - timezone.timedelta(days=30)
    current_month_count = Appointment.objects.filter(doctor=doctor, appointment_date__gte=thirty_days_ago).count()
    prev_month_count = Appointment.objects.filter(
        doctor=doctor, 
        appointment_date__lt=thirty_days_ago, 
        appointment_date__gte=thirty_days_ago - timezone.timedelta(days=30)
    ).count()
    
    growth = 0
    if prev_month_count > 0:
        growth = ((current_month_count - prev_month_count) / prev_month_count) * 100
    else:
        growth = 100 if current_month_count > 0 else 0
        
    # Visit completion
    total_appts = Appointment.objects.filter(doctor=doctor).count()
    completed_appts = Appointment.objects.filter(doctor=doctor, status='completed').count()
    completion_rate = (completed_appts / total_appts * 100) if total_appts > 0 else 0

    # Colors for avatars
    bg_colors = ['#ebf8ff', '#fef3c7', '#f1f1f1', '#eef2ff', '#fdf2f2', '#f0fdf4']
    text_colors = ['#3182ce', '#d97706', '#4a5568', '#4f46e5', '#9b1c1c', '#166534']

    # Transform patients for template
    patients_list = []
    for p in patients_page:
        # Generate hash id
        h = hashlib.md5(p['patient_name'].encode()).hexdigest()
        p['hash_id'] = f"{int(h, 16) % 10000:04d}"
        
        # Initials
        name_parts = p['patient_name'].split()
        p['initials'] = (name_parts[0][0] + (name_parts[-1][0] if len(name_parts) > 1 else "")) if name_parts else "P"
        p['initials'] = p['initials'].upper()
        
        # Random but consistent color based on name
        color_idx = int(h, 16) % len(bg_colors)
        p['avatar_bg'] = bg_colors[color_idx]
        p['avatar_color'] = text_colors[color_idx]
        
        # Check for history to determine New/Returning status
        has_history = Appointment.objects.filter(
            doctor=doctor,
            patient_name__iexact=p['patient_name'],
            status='completed'
        ).count() > 1
        
        # Optionally, get status of last appointment
        last_appt = Appointment.objects.filter(doctor=doctor, patient_name=p['patient_name'], appointment_date=p['last_visit']).first()
        p['last_visit_status'] = last_appt.status.title() if last_appt else ("Returning" if has_history else "New")
        
        patients_list.append(p)

    return render(request, 'doctors/my_patients.html', {
        'doctor': doctor,
        'patients': patients_page, # Page object for pagination
        'patients_data': patients_list, # List for table
        'total_active': total_active,
        'total_patients': total_active, # Support both names
        'monthly_growth': round(growth, 1),
        'completion_rate': round(completion_rate, 1),
        'start_date': start_date,
        'end_date': end_date,
        'search_query': search_query
    })

@login_required
@role_required('doctor')
def patient_history_view(request, patient_name):
    """Details of a specific patient's history with this doctor"""
    doctor = Doctor.objects.get(user=request.user)
    appointments = Appointment.objects.filter(
        doctor=doctor, 
        patient_name=patient_name
    ).order_by('-appointment_date')
    
    return render(request, 'doctors/patient_history.html', {
        'patient_name': patient_name,
        'appointments': appointments
    })


@login_required
@login_required
@role_required('doctor')
def edit_my_profile(request):
    """Allow doctors to edit their own profile (Restricted Fields)"""
    doctor = Doctor.objects.get(user=request.user)
    
    if request.method == 'POST':
        try:
            with transaction.atomic():
                # Doctors can update their own: Name, Specialization
                doctor.name = request.POST.get('name', doctor.name)
                doctor.specialization = request.POST.get('specialization', doctor.specialization)
                
                # Update Department
                department_id = request.POST.get('department')
                if department_id:
                     department = Department.objects.filter(id=department_id, hospital=doctor.hospital).first()
                     if department:
                         doctor.department = department

                # Update Treatments
                treatment_ids = request.POST.getlist('treatments')
                if treatment_ids:
                    # Validate treatments belong to the doctor's hospital
                    treatments_to_add = Treatment.objects.filter(id__in=treatment_ids, hospital=doctor.hospital)
                    doctor.treatments.set(treatments_to_add)
                elif 'treatments' in request.POST: # Only clear if checkbox group was present
                    doctor.treatments.clear()


                doctor.save()

                # Profile Details
                # Check if profile exists; if not, create it
                if hasattr(doctor.user, 'doctorprofile'):
                    profile = doctor.user.doctorprofile
                else:
                    # Create new profile with default values for required fields
                    profile = DoctorProfile(
                        user=doctor.user,
                        gender='Other',
                        date_of_birth=timezone.now().date(),
                        contact_number='',
                        address='',
                        qualification='',
                        specialization=doctor.specialization,
                        year_of_experience=0,
                        aadhaar='', # Assuming generic default
                        medical_certificate='',
                        registration_certificate='',
                        degree_certificates=''
                    )

                # Update fields with submitted data
                profile.contact_number = request.POST.get('contact_number', profile.contact_number)
                profile.gender = request.POST.get('gender', profile.gender)
                profile.qualification = request.POST.get('qualification', profile.qualification)
                
                # Careful with integer conversion for year_of_experience
                yoe = request.POST.get('year_of_experience')
                if yoe:
                    profile.year_of_experience = int(yoe)
                
                profile.address = request.POST.get('address', profile.address)
                
                dob = request.POST.get('date_of_birth')
                if dob:
                    profile.date_of_birth = dob

                # Handle Photo Upload
                if request.FILES.get('passport_photo'):
                    profile.passport_photo = request.FILES.get('passport_photo')
                
                profile.save()

                # User Phone
                phone = request.POST.get('contact_number')
                if phone:
                    doctor.user.phone = phone
                    doctor.user.save()
            
            messages.success(request, 'Profile updated successfully.')
            return redirect('doctor_profile_edit')

        except Exception as e:
            messages.error(request, f'Error updating profile: {str(e)}')
            return redirect('doctor_profile_edit')

    # GET Request
    # Fetch all departments for this hospital to populate dropdown
    departments = Department.objects.filter(hospital=doctor.hospital)

    return render(request, 'doctors/edit_my_profile.html', {
        'doctor': doctor,
        'departments': departments,
    })


@login_required
@role_required('doctor')
def patient_history_partial(request, patient_name):
    """
    Returns HTML fragment for patient history (timeline).
    Used for AJAX loading in the dashboard.
    """
    doctor = Doctor.objects.get(user=request.user)
    appointments = Appointment.objects.filter(
        doctor=doctor, 
        patient_name__iexact=patient_name
    ).order_by('-appointment_date')
    
    return render(request, 'doctors/partials/patient_history_partial.html', {
        'patient_name': patient_name,
        'appointments': appointments
    })

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_hospital_queue_status(request):
    """
    Returns queue status for all doctors in the admin's hospital.
    Only includes doctors who have at least one appointment scheduled for TODAY.
    """
    try:
        # 1. Get Hospital
        if hasattr(request.user, 'hospitaladmin'):
             hospital = request.user.hospitaladmin.hospital
        else:
             return Response({'error': 'Unauthorized'}, status=403)

        today = timezone.localtime().date()
        
        # 2. Get doctors with appointments today
        # We query Appointment to find unique doctors who have appointments today
        # This implicitly filters out doctors with no appointments
        doctor_ids = Appointment.objects.filter(
            hospital=hospital,
            appointment_date__date=today
        ).values_list('doctor', flat=True).distinct()
        
        doctors_with_appointments = Doctor.objects.filter(id__in=doctor_ids)

        queue_data = []
        
        for doctor in doctors_with_appointments:
            # Get Queue
            queue, _ = DailyQueue.objects.get_or_create(doctor=doctor, date=today)
            current_token = queue.current_token
            
            # Get Next Token (First scheduled appointment > current_token)
            next_appt = Appointment.objects.filter(
                doctor=doctor,
                appointment_date__date=today,
                token_number__gt=current_token,
                status__in=['scheduled', 'confirmed']
            ).order_by('token_number').first()
            
            next_token_display = f"#{next_appt.token_number}" if next_appt else "--"
            
            # Use doctor profile image if available
            doctor_image = None
            if hasattr(doctor.user, 'doctorprofile') and doctor.user.doctorprofile.passport_photo:
                doctor_image = doctor.user.doctorprofile.passport_photo.url
            
            queue_data.append({
                'doctor_name': doctor.name,
                'specialization': doctor.specialization,
                'current_token': current_token,
                'next_token': next_token_display,
                'doctor_image': doctor_image
            })
            
        return Response({'success': True, 'queue': queue_data})

    except Exception as e:
        return Response({'success': False, 'error': str(e)}, status=500)