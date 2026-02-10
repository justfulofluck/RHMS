from django.contrib.auth import get_user_model
User = get_user_model()
from django.http import JsonResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth import authenticate, login
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.utils.encoding import force_bytes, force_str
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.core.mail import send_mail
from django.utils import timezone
from datetime import timedelta
from django.db.models import Count, Q
from rest_framework import status, generics
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from django.contrib.auth.decorators import login_required, user_passes_test

from hospitals.models import Hospital, HospitalAdmin
from doctors.models import Doctor
from appointments.models import Appointment
from .serializers import PasswordResetRequestSerializer, PasswordResetConfirmSerializer
from django.db.models.functions import TruncDate, TruncMonth
from django.db.models import Count
from django import forms
import csv
from django.http import HttpResponse


User = get_user_model()

class PasswordResetRequestView(generics.GenericAPIView):
    permission_classes = [AllowAny]
    serializer_class = PasswordResetRequestSerializer

    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        email = serializer.validated_data['email']

        try:
            user = User.objects.get(email=email)
            print(f"DEBUG: User found for email {email}")
        except User.DoesNotExist:
            print(f"DEBUG: No user found for email {email}")
            return Response({"message": "If this email exists, a reset link has been sent."}, status=status.HTTP_200_OK)

        token = PasswordResetTokenGenerator().make_token(user)
        uid = urlsafe_base64_encode(force_bytes(user.pk))
        
        # Dynamic host
        current_site = request.get_host()
        reset_link = f"http://{current_site}/reset-password-confirm/?uid={uid}&token={token}"
        
        print(f"DEBUG: Attempting to send email to {email}...")
        try:
            send_mail(
                subject="Password Reset Request",
                message=f"Click the link to reset your password: {reset_link}",
                from_email=None,
                recipient_list=[email],
                fail_silently=False,
            )
            print("DEBUG: Mail sent successfully via SMTP.")
        except Exception as e:
            print(f"DEBUG: Mail sending FAILED. Error: {e}")
            # We still return 200 to avoid leaking info, but logs will show error
            return Response({"message": "If this email exists, a reset link has been sent."}, status=status.HTTP_200_OK)

        return Response({"message": "If this email exists, a reset link has been sent."}, status=status.HTTP_200_OK)

class PasswordResetConfirmView(generics.GenericAPIView):
    permission_classes = [AllowAny]
    serializer_class = PasswordResetConfirmSerializer

    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        uid = serializer.validated_data['uid']
        token = serializer.validated_data['token']
        new_password = serializer.validated_data['new_password']

        try:
            user_id = force_str(urlsafe_base64_decode(uid))
            user = User.objects.get(pk=user_id)
        except (User.DoesNotExist, ValueError, TypeError):
            return Response({"error": "Invalid link"}, status=status.HTTP_400_BAD_REQUEST)

        if not PasswordResetTokenGenerator().check_token(user, token):
            return Response({"error": "Invalid or expired token"}, status=status.HTTP_400_BAD_REQUEST)

        user.set_password(new_password)
        user.save()
        return Response({"message": "Password has been reset successfully"}, status=status.HTTP_200_OK)

def universal_login_view(request):
    """
    Universal login view that handles all user roles (doctor, hospital_admin, superadmin)
    Redirects users to appropriate dashboard based on their role
    """
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
        user = authenticate(request, username=email, password=password)
        
        if user:
            login(request, user)
            # Redirect based on user role
            if user.role == 'doctor':
                return redirect('doctor_dashboard')
            elif user.role == 'hospital_admin':
                return redirect('hospital_admin_dashboard')
            elif user.is_superuser:
                return redirect('admin:index')  # Django admin
            else:
                messages.error(request, f'Invalid user role: {user.role}')
        else:
            # Provide more specific error message
            try:
                user_obj = User.objects.get(email=email)
                if not user_obj.is_active:
                    messages.error(request, 'Your account is inactive. Please contact support.')
                elif user_obj.role not in ['doctor', 'hospital_admin'] and not user_obj.is_superuser:
                    messages.error(request, 'Your account type is not authorized for portal access.')
                else:
                    messages.error(request, 'Invalid password. Please try again.')
            except User.DoesNotExist:
                messages.error(request, 'No account found with this email address.')
    
    return render(request, 'frontend/universal_login.html')

def superadmin_login_ajax(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')

        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            return JsonResponse({'success': False, 'error': 'User not found'})

        if user.is_superuser:
            user = authenticate(request, username=email, password=password)
            if user is not None:
                login(request, user)
                return JsonResponse({'success': True, 'redirect_url': '/accounts/superadmin/dashboard/'})
            else:
                return JsonResponse({'success': False, 'error': 'Invalid password'})
        else:
            return JsonResponse({'success': False, 'error': 'Not a super admin'})

    return render(request, 'accounts/superadmin_login.html')

def logout_view(request):
    from django.contrib.auth import logout
    logout(request)
    return redirect('homepage')

def is_superadmin(user):
    return user.is_authenticated and user.is_superuser

class AppointmentFilterForm(forms.Form):
    start_date = forms.DateField(required=False, widget=forms.DateInput(attrs={'type': 'date'}))
    end_date = forms.DateField(required=False, widget=forms.DateInput(attrs={'type': 'date'}))
    doctor = forms.ModelChoiceField(queryset=Doctor.objects.all(), required=False)
    hospital = forms.ModelChoiceField(queryset=Hospital.objects.all(), required=False)

@login_required
@user_passes_test(is_superadmin)
def superadmin_dashboard(request):
    today = timezone.now().date()
    start_of_week = today - timedelta(days=today.weekday())
    start_of_month = today.replace(day=1)
    today_start = timezone.localtime().replace(hour=0, minute=0, second=0, microsecond=0)
    today_end = today_start + timedelta(days=1)

    form = AppointmentFilterForm(request.GET)
    appointments = Appointment.objects.all()

    if form.is_valid():
        if form.cleaned_data['start_date']:
            appointments = appointments.filter(created_at__gte=form.cleaned_data['start_date'])
        if form.cleaned_data['end_date']:
            appointments = appointments.filter(created_at__lte=form.cleaned_data['end_date'])
        if form.cleaned_data['doctor']:
            appointments = appointments.filter(doctor=form.cleaned_data['doctor'])
        if form.cleaned_data['hospital']:
            appointments = appointments.filter(hospital=form.cleaned_data['hospital'])

    context = {
        'total_users': User.objects.count(),
        'total_doctors': User.objects.filter(role='doctor').count(),
        'total_hospitals': Hospital.objects.count(),
        'total_appointments': Appointment.objects.count(),
        'new_users_week': User.objects.filter(date_joined__date__gte=start_of_week).count(),
        'new_users_month': User.objects.filter(date_joined__date__gte=start_of_month).count(),
        'appointments_today': Appointment.objects.filter(created_at__range=(today_start, today_end)).count(),
        'top_doctors': Doctor.objects.annotate(total_appointments=Count('appointments')).order_by('-total_appointments')[:5],
        'top_hospitals': Hospital.objects.annotate(total_appointments=Count('appointments')).order_by('-total_appointments')[:5],
        'recent_users': User.objects.order_by('-date_joined')[:5],
        'recent_appointments': Appointment.objects.order_by('-created_at')[:5],
    }

    pending_hospitals = Hospital.objects.filter(status=Hospital.STATUS_PENDING)
    approved_hospitals = Hospital.objects.filter(status=Hospital.STATUS_APPROVED)



    # Appointment trends (last 7 days)
    last_7_days = timezone.now() - timedelta(days=6)
    appointment_by_day = (
        Appointment.objects.filter(created_at__gte=last_7_days)
        .annotate(day=TruncDate('created_at'))
        .values('day')
        .annotate(count=Count('id'))
        .order_by('day')
    )
    chart_labels = [entry['day'].strftime('%b %d') for entry in appointment_by_day]
    chart_data = [entry['count'] for entry in appointment_by_day]

    # Doctor registrations (last 12 months)
    twelve_months_ago = timezone.now() - timedelta(days=365)
    doctor_monthly = (
        User.objects
        .filter(role='doctor', date_joined__gte=twelve_months_ago)
        .annotate(month=TruncMonth('date_joined'))
        .values('month')
        .annotate(count=Count('id'))
        .order_by('month')
    )
    doctor_chart_labels = [entry['month'].strftime('%b %Y') for entry in doctor_monthly]
    doctor_chart_data = [entry['count'] for entry in doctor_monthly]

    # User role distribution
    role_distribution = (
        User.objects
        .values('role')
        .annotate(count=Count('id'))
        .order_by('role')
    )
    role_labels = [entry['role'].capitalize() for entry in role_distribution]
    role_counts = [entry['count'] for entry in role_distribution]

    context.update({
        'chart_labels': chart_labels,
        'chart_data': chart_data,
        'doctor_chart_labels': doctor_chart_labels,
        'doctor_chart_data': doctor_chart_data,
        'role_labels': role_labels,
        'role_counts': role_counts,
        'filter_form': form,
        'filtered_appointments': appointments.order_by('-appointment_date')[:10],
        'pending_hospitals': pending_hospitals,
        'approved_hospitals': approved_hospitals,
        'hospital_admins': User.objects.filter(role='hospital_admin'),
        'doctors': User.objects.filter(role='doctor'),
    })

    return render(request, 'accounts/superadmin_dashboard.html', context)

@login_required
@login_required
@user_passes_test(is_superadmin)
def delete_user(request, user_id):
    if request.method == 'POST':
        user = get_object_or_404(User, id=user_id)
        
        # If user is a hospital admin, delete the hospital as well
        if hasattr(user, 'hospitaladmin'):
            hospital = user.hospitaladmin.hospital
            hospital.delete() # This will cascade delete the HospitalAdmin as well
            user.delete() # Explicitly delete the user
            messages.success(request, f'Hospital {hospital.name} and Admin User deleted successfully.')
        else:
            user.delete()
            messages.success(request, 'User deleted successfully.')
            
    return redirect('superadmin_dashboard')

@login_required
@user_passes_test(is_superadmin)
def manage_registrations(request):
    pending_hospitals = Hospital.objects.filter(is_approved=False)
    pending_doctors = Doctor.objects.filter(is_approved=False)

    if request.method == 'POST':
        entity_type = request.POST.get('type')
        entity_id = request.POST.get('id')
        action = request.POST.get('action')

        if entity_type == 'hospital':
            hospital = Hospital.objects.get(id=entity_id)
            hospital.is_approved = (action == 'approve')
            hospital.save()
            
            if hospital.is_approved:
                try:
                    hospital_admin = HospitalAdmin.objects.get(hospital=hospital)
                    hospital_admin.user.role = 'hospital_admin'
                    hospital_admin.user.is_active = True
                    hospital_admin.user.save()
                except HospitalAdmin.DoesNotExist:
                    pass
        elif entity_type == 'doctor':
            doctor = Doctor.objects.get(id=entity_id)
            doctor.is_approved = (action == 'approve')
            doctor.save()

        return redirect('manage_registrations')

    return render(request, 'accounts/manage_registrations.html', {
        'pending_hospitals': pending_hospitals,
        'pending_doctors': pending_doctors,
    })

@login_required
@user_passes_test(is_superadmin)
def export_appointments_csv(request):
    form = AppointmentFilterForm(request.GET)
    appointments = Appointment.objects.all()

    if form.is_valid():
        if form.cleaned_data['start_date']:
            appointments = appointments.filter(created_at__gte=form.cleaned_data['start_date'])
        if form.cleaned_data['end_date']:
            appointments = appointments.filter(created_at__lte=form.cleaned_data['end_date'])
        if form.cleaned_data['doctor']:
            appointments = appointments.filter(doctor=form.cleaned_data['doctor'])
        if form.cleaned_data['hospital']:
            appointments = appointments.filter(hospital=form.cleaned_data['hospital'])

    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="appointments.csv"'

    writer = csv.writer(response)
    writer.writerow(['Patient', 'Doctor', 'Hospital', 'Date', 'Token'])

    for appt in appointments:
        writer.writerow([
            appt.patient_name,
            appt.doctor.user.email,
            appt.hospital.name,
            appt.appointment_date,
            appt.token_number or 'N/A'
        ])

    return response

@login_required
@user_passes_test(is_superadmin)
def superadmin_search(request):
    try:
        query = request.GET.get('q', '').strip()
        print(f"DEBUG: Search Query: '{query}'") # DEBUG LOG
        
        if not query:
            return JsonResponse({'results': []})

        results = []

        # 1. Search Users (Email)
        # Ensure User is defined (using global variable from top of file)
        # Check if role field exists on User model to be safe
        users = User.objects.filter(email__icontains=query).values('id', 'email', 'role')[:5]
        print(f"DEBUG: Found {len(users)} users") # DEBUG LOG
        
        for u in users:
            results.append({
                'category': 'User',
                'label': f"{u['email']} ({u.get('role', 'N/A')})",
                'id': u['id'],
                'type': 'user'
            })

        # 2. Search Hospitals
        hospitals = Hospital.objects.filter(
            Q(name__icontains=query) | Q(city__icontains=query)
        ).values('id', 'name', 'city')[:5]
        print(f"DEBUG: Found {len(hospitals)} hospitals") # DEBUG LOG

        for h in hospitals:
            results.append({
                'category': 'Hospital',
                'label': f"{h['name']} - {h['city']}",
                'id': h['id'],
                'type': 'hospital'
            })

        # 3. Search Doctors
        doctors = Doctor.objects.filter(
            Q(name__icontains=query) | Q(specialization__icontains=query)
        ).values('id', 'name', 'specialization')[:5]
        print(f"DEBUG: Found {len(doctors)} doctors") # DEBUG LOG

        for d in doctors:
            results.append({
                'category': 'Doctor',
                'label': f"Dr. {d['name']} ({d['specialization']})",
                'id': d['id'],
                'type': 'doctor'
            })

        return JsonResponse({'results': results})
    
    except Exception as e:
        import traceback
        traceback.print_exc() # Print stack trace to console
        print(f"ERROR in superadmin_search: {str(e)}")
        return JsonResponse({'error': str(e)}, status=500)

@login_required
@user_passes_test(is_superadmin)
def user_management(request):
    from django.core.paginator import Paginator
    
    tab = request.GET.get('tab', 'admins') # 'admins' or 'doctors'
    page_number = request.GET.get('page')
    
    if tab == 'doctors':
        queryset = Doctor.objects.select_related('user', 'hospital').all().order_by('-id')
    else:
        queryset = HospitalAdmin.objects.select_related('user', 'hospital').all().order_by('-id')

    paginator = Paginator(queryset, 10) # 10 items per page
    page_obj = paginator.get_page(page_number)

    context = {
        'page_obj': page_obj,
        'tab': tab,
    }
    return render(request, 'accounts/user_management.html', context)

@login_required
@user_passes_test(is_superadmin)
def appointment_management(request):
    from django.core.paginator import Paginator
    
    page_number = request.GET.get('page')
    queryset = Appointment.objects.select_related('doctor', 'doctor__user').all().order_by('-appointment_date')

    paginator = Paginator(queryset, 10) # 10 items per page
    page_obj = paginator.get_page(page_number)

    context = {
        'page_obj': page_obj,
    }
    return render(request, 'accounts/appointment_management.html', context)

@login_required
@user_passes_test(is_superadmin)
def pending_approvals(request):
    # Fetch pending hospitals
    pending_hospitals = Hospital.objects.filter(status=Hospital.STATUS_PENDING).order_by('-created_at')
    
    # Handle Approve/Reject actions
    if request.method == 'POST':
        hospital_id = request.POST.get('hospital_id')
        action = request.POST.get('action')
        
        try:
            hospital = Hospital.objects.get(id=hospital_id)
            if action == 'approve':
                hospital.status = Hospital.STATUS_APPROVED
                hospital.is_approved = True
                hospital.save()
                
                # Activate the admin user
                try:
                    hospital_admin = HospitalAdmin.objects.get(hospital=hospital)
                    hospital_admin.user.is_active = True
                    hospital_admin.user.save()
                except HospitalAdmin.DoesNotExist:
                    pass
                    
                messages.success(request, f'{hospital.name} has been approved.')
                
            elif action == 'reject':
                hospital.status = Hospital.STATUS_REJECTED
                hospital.is_approved = False
                hospital.save()
                messages.warning(request, f'{hospital.name} has been rejected.')
                
        except Hospital.DoesNotExist:
            messages.error(request, 'Hospital not found.')
            
        return redirect('pending_approvals')

    context = {
        'pending_hospitals': pending_hospitals,
    }
    return render(request, 'accounts/pending_approvals.html', context)

@login_required
@user_passes_test(is_superadmin)
def delete_appointment(request, appointment_id):
    if request.method == 'POST':
        try:
            appointment = Appointment.objects.get(id=appointment_id)
            appointment.delete()
            messages.success(request, 'Appointment deleted successfully.')
        except Appointment.DoesNotExist:
            messages.error(request, 'Appointment not found.')
        except Exception as e:
            messages.error(request, f'Error deleting appointment: {str(e)}')
    
    return redirect('appointment_management')