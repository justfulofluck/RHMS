from django.contrib.auth import get_user_model
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
from django.db.models import Count
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
        except User.DoesNotExist:
            return Response({"message": "If this email exists, a reset link has been sent."}, status=status.HTTP_200_OK)

        token = PasswordResetTokenGenerator().make_token(user)
        uid = urlsafe_base64_encode(force_bytes(user.pk))
        reset_link = f"http://192.168.1.208:8000/reset-password-confirm/?uid={uid}&token={token}"

        send_mail(
            subject="Password Reset Request",
            message=f"Click the link to reset your password: {reset_link}",
            from_email=None,
            recipient_list=[email],
        )

        print("mail sent to user")
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
    chat_labels = [entry['day'].strftime('%b %d') for entry in appointment_by_day]
    chat_data = [entry['count'] for entry in appointment_by_day]

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
        'chat_labels': chat_labels,
        'chat_data': chat_data,
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