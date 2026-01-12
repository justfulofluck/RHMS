from datetime import datetime, date, timedelta
from django.db.models import Q
from django.core.mail import send_mail
from django.http import JsonResponse
from django.shortcuts import render, get_object_or_404
from django.utils import timezone
from rest_framework import viewsets, permissions
from rest_framework.decorators import action, api_view, permission_classes
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST
from django.utils.decorators import method_decorator
from notifications.signals import notify
import uuid # Added for uuid.uuid4()

from core.permissions import IsSuperAdmin, IsHospitalAdminOfSameHospital, IsSelfDoctor
from appointments.models import Appointment, DoctorAvailability
from patients.models import Patient
from appointments.serializers import AppointmentSerializer, DoctorAvailabilitySerializer
from doctors.models import Doctor
from hospitals.models import Hospital
from django.contrib.auth import get_user_model

User = get_user_model()

# ... (rest of imports)

# ...

# 🔐 Permissions
class IsHospitalAdminOrReadOnly(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return True
        return request.user and request.user.is_authenticated


# 📅 Doctor Availability API
class DoctorAvailabilityViewSet(viewsets.ModelViewSet):
    queryset = DoctorAvailability.objects.select_related('doctor').all()
    serializer_class = DoctorAvailabilitySerializer
    permission_classes = [IsHospitalAdminOrReadOnly]

    def get_permissions(self):
        if self.action in ['create', 'update', 'partial_update', 'destroy']:
            return [permissions.IsAuthenticated(), IsSuperAdmin() | IsHospitalAdminOfSameHospital() | IsSelfDoctor()]
        return [permissions.IsAuthenticated()]

    def get_queryset(self):
        user = self.request.user
        department = self.request.query_params.get('department')
        qs = super().get_queryset()

        if hasattr(user, 'patient'):
            # Patients should only see availability for doctors in their hospital or all if no hospital
            if hasattr(user.patient, 'hospital') and user.patient.hospital:
                qs = qs.filter(doctor__hospital=user.patient.hospital)
            if department:
                qs = qs.filter(doctor__department__name__icontains=department)
        elif hasattr(user, 'doctor'):
            qs = qs.filter(doctor=user.doctor)
        elif hasattr(user, 'hospital_admin'):
            qs = qs.filter(doctor__hospital=user.hospital_admin.hospital)
        elif user.is_superuser:
            return qs
        else: # Unauthenticated users or other roles
            # For public view, maybe filter by hospital if provided, or show all
            hospital_id = self.request.query_params.get('hospital_id')
            if hospital_id:
                qs = qs.filter(doctor__hospital_id=hospital_id)
            if department:
                qs = qs.filter(doctor__department__name__icontains=department)
            
        return qs

    def perform_create(self, serializer):
        doctor = serializer.validated_data['doctor']
        date = serializer.validated_data['date']
        start = serializer.validated_data['start_time']
        end = serializer.validated_data['end_time']

        if start >= end:
            raise ValueError("Start time must be before end time.")

        overlap = DoctorAvailability.objects.filter(
            doctor=doctor, date=date
        ).filter(
            Q(start_time__lt=end) & Q(end_time__gt=start)
        ).exists()

        if overlap:
            raise ValueError("Overlapping availability for this doctor on the given date.")

        serializer.save()

# 📆 Calendar View for Doctors & Patients
class CalendarView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user
        start_date = request.query_params.get('start')
        end_date = request.query_params.get('end')
        events = []

        availability_qs = DoctorAvailability.objects.all()
        appointment_qs = Appointment.objects.all()

        if start_date and end_date:
            availability_qs = availability_qs.filter(date__range=[start_date, end_date])
            appointment_qs = appointment_qs.filter(appointment_date__date__range=[start_date, end_date])

        if hasattr(user, 'doctor'):
            availability_qs = availability_qs.filter(doctor=user.doctor)
            appointment_qs = appointment_qs.filter(doctor=user.doctor)
        elif hasattr(user, 'patient'):
            appointment_qs = appointment_qs.filter(patient_name=user.get_full_name())

        for slot in availability_qs:
            events.append({
                "title": "Available",
                "start": f"{slot.date}T{slot.start_time}",
                "end": f"{slot.date}T{slot.end_time}",
                "color": "#28a745"
            })

        for appt in appointment_qs:
            events.append({
                "title": f"Booked with Dr. {appt.doctor.name}",
                "start": appt.appointment_date.isoformat(),
                "end": (appt.appointment_date + timezone.timedelta(minutes=15)).isoformat(),
                "color": "#dc3545"
            })

        return Response(events)


# 📱 Mobile Booking API (Authenticated)
class MobileBookingView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        availability_id = request.data.get('availability_id')
        try:
            slot = DoctorAvailability.objects.get(id=availability_id, is_available=True)
        except DoctorAvailability.DoesNotExist:
            return Response({"error": "Slot not available"}, status=400)

        appointment = Appointment.objects.create(
            patient_name=request.user.get_full_name(),
            doctor=slot.doctor,
            hospital=slot.doctor.hospital,
            appointment_date=datetime.combine(slot.date, slot.start_time),
            created_at=timezone.now()
        )
        slot.is_available = False
        slot.save()

        return Response({
            "message": "Appointment booked",
            "doctor": slot.doctor.name,
            "date": slot.date,
            "start": slot.start_time,
            "end": slot.end_time
        })


# 📄 Public Booking via AJAX (Unauthenticated)
@csrf_exempt
@require_POST
def book_appointment_ajax(request):
    try:
        name = request.POST['name']
        age = int(request.POST['age'])
        gender = request.POST['gender']
        contact = request.POST['contact_number']
        address = request.POST['address']
        doctor_id = request.POST['doctor_id']
        hospital_id = request.POST['hospital_id']
        appointment_date = request.POST['appointment_date']
        email = request.POST.get('email', f"{contact}@example.com") # Fallback email

        # Create User
        user, created = User.objects.get_or_create(email=email, defaults={
            'role': 'patient',
            'is_active': True
        })
        if created:
            user.set_unusable_password()
            user.save()

        # Save patient
        patient, _ = Patient.objects.get_or_create(
            user=user,
            defaults={
                'age': age,
                'gender': gender,
                'phone': contact,
                'address': address
            }
        )

        # Save appointment
        doctor = Doctor.objects.get(id=doctor_id)
        hospital = Hospital.objects.get(id=hospital_id)
        
        # ✅ Verify hospital is approved before allowing booking
        if hospital.status != Hospital.STATUS_APPROVED:
            return JsonResponse({
                'success': False, 
                'error': 'This hospital is not currently accepting appointments.'
            }, status=400)
        
        appointment_datetime = datetime.fromisoformat(appointment_date)
        token = str(uuid.uuid4())[:8]

        new_appointment = Appointment.objects.create(
            hospital=hospital,
            doctor=doctor,
            patient_name=patient.name,
            appointment_date=appointment_datetime,
            created_at=timezone.now(),
            status='scheduled'  # Default status
        )
        
        # Send notification to Doctor
        # For unauthenticated requests, the sender can be the patient's user object or a system user
        sender = patient.user if patient.user else None # Assuming patient always has a user
        if not sender: # Fallback if patient.user is somehow None
            sender = new_appointment # Use the appointment instance itself as sender

        notify.send(
            sender, 
            recipient=doctor.user, 
            verb='booked an appointment', 
            target=new_appointment,
            description=f"New appointment with {name} on {appointment_datetime.strftime('%Y-%m-%d %H:%M')}"
        )

        return JsonResponse({
            'success': True,
            'token': token,
            'time': appointment_datetime.strftime('%I:%M %p, %d %b %Y')
        })

    except Exception as e:
        return JsonResponse({'success': False, 'error': str(e)})


# 📋 My Appointments (Authenticated)
class MyAppointmentsViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = AppointmentSerializer
    #permission_classes = [IsAuthenticated]
    permission_classes = [permissions.AllowAny]
    def get_queryset(self):
        return Appointment.objects.filter(patient_name=self.request.user.get_full_name())

def get_available_slots(request):
    doctor_id = request.GET.get('doctor_id')
    if not doctor_id:
        return JsonResponse({'error': 'Doctor ID is required'}, status=400)

    today = date.today()
    end_date = today + timedelta(days=4)

    slots = DoctorAvailability.objects.filter(
        doctor_id=doctor_id,
        date__range=(today, end_date),
        is_available=True
    ).order_by('date', 'start_time')

    slot_data = []
    for slot in slots:
        slot_data.append({
            'id': slot.id,
            'date': slot.date.strftime('%Y-%m-%d'),
            'start_time': slot.start_time.strftime('%H:%M'),
            'end_time': slot.end_time.strftime('%H:%M'),
        })

    return JsonResponse({'slots': slot_data})

class AppointmentViewSet(viewsets.ModelViewSet):  # ✅ Correct name
    queryset = Appointment.objects.all()
    serializer_class = AppointmentSerializer
    #permission_classes = [permissions.IsAuthenticated]
    permission_classes = [permissions.AllowAny]

    def get_queryset(self):
        user = self.request.user
        if user.is_authenticated:
            return Appointment.objects.filter(patient_name=self.request.user.get_full_name())
        return Appointment.objects.all()

@csrf_exempt
@require_POST
def cancel_appointment(request, appointment_id):
    """Cancel an appointment"""
    try:
        appointment = Appointment.objects.get(id=appointment_id)
        
        # Check permissions (optional - for now public with ID, but should be secured in production)
        # In a real app, we'd verify the user owns this appointment
        
        if appointment.status == 'cancelled':
            return JsonResponse({'error': 'Appointment is already cancelled'}, status=400)
            
        # Update status
        appointment.status = 'cancelled'
        appointment.cancelled_at = timezone.now()
        appointment.cancellation_reason = request.POST.get('reason', 'Cancelled by user')
        appointment.save()
        
        # Send notification to Doctor
        # Assuming the cancellation is initiated by the patient or a system process
        sender = request.user if request.user.is_authenticated else None
        if not sender:
            # Fallback for unauthenticated cancellation (e.g., via a public link)
            # You might want a dedicated system user for this or infer from appointment.patient
            sender = appointment.patient.user if hasattr(appointment, 'patient') and appointment.patient else None
            if not sender:
                sender = appointment # Use the appointment instance itself as sender

        notify.send(
            sender,
            recipient=appointment.doctor.user,
            verb='cancelled an appointment',
            target=appointment,
            description=f"Appointment with {appointment.patient_name} on {appointment.appointment_date.strftime('%Y-%m-%d %H:%M')} has been cancelled."
        )

        # Send email to patient
        # We need to find the patient's email. 
        # In the current model, we don't store email directly on Appointment, 
        # but we might have a User/Patient linked.
        # For this implementation, we'll assume we can't send email unless we have the address.
        # If we stored email on appointment creation (we should!), we'd use it here.
        
        return JsonResponse({
            'success': True, 
            'message': 'Appointment cancelled successfully',
            'status': 'cancelled'
        })
        
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)

# 📱 Phase 7: Mobile Patient Booking Views

def mobile_booking_view(request, doctor_id):
    """Renders the mobile booking page for a specific doctor"""
    doctor = get_object_or_404(Doctor, id=doctor_id)
    return render(request, 'appointments/mobile_booking.html', {
        'doctor': doctor
    })

def get_mobile_slots(request, doctor_id):
    """Returns availability slots for today, tomorrow, and day after (3 days)"""
    try:
        doctor = Doctor.objects.get(id=doctor_id)
        today = timezone.localtime().date()
        days_data = []

        for i in range(3):
            target_date = today + timedelta(days=i)
            
            # Fetch slots
            slots = DoctorAvailability.objects.filter(
                doctor=doctor,
                date=target_date,
                is_available=True
            ).order_by('start_time')
            
            slot_list = []
            for slot in slots:
                slot_list.append({
                    'id': slot.id,
                    'start': slot.start_time.strftime('%I:%M %p'),
                    'end': slot.end_time.strftime('%I:%M %p'),
                })
            
            # Determine label
            if i == 0:
                label = "Today"
            elif i == 1:
                label = "Tomorrow"
            else:
                label = target_date.strftime('%a, %d %b') # e.g., "Mon, 12 Dec"

            days_data.append({
                'date': target_date.strftime('%Y-%m-%d'),
                'label': label,
                'slots': slot_list
            })
            
        return JsonResponse({'success': True, 'days': days_data})
        
    except Doctor.DoesNotExist:
        return JsonResponse({'success': False, 'error': 'Doctor not found'})
    except Exception as e:
        return JsonResponse({'success': False, 'error': str(e)})
# 🏥 Queue Management APIs (Doctor Console)
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_queue_status(request):
    try:
        doctor = request.user.doctor
        today = timezone.localtime().date()
        
        queue, _ = DailyQueue.objects.get_or_create(doctor=doctor, date=today)
        
        # Get current appointment details if token > 0
        patient_name = None
        visit_status = None
        
        if queue.current_token > 0:
            current_appt = Appointment.objects.filter(
                doctor=doctor,
                appointment_date__date=today,
                token_number=queue.current_token
            ).first()
            
            if current_appt:
                patient_name = current_appt.patient_name
                
                # Check history logic (Duplicated from dashboard view for consistency)
                has_history = False
                if current_appt.patient_email:
                     has_history = Appointment.objects.filter(
                        doctor=doctor,
                        patient_email=current_appt.patient_email,
                        status='completed'
                    ).exclude(id=current_appt.id).exists()
                else: 
                     has_history = Appointment.objects.filter(
                        doctor=doctor,
                        patient_name__iexact=current_appt.patient_name,
                        status='completed'
                    ).exclude(id=current_appt.id).exists()
                    
                visit_status = "Returning" if has_history else "New"

        return Response({
            'current_token': queue.current_token,
            'patient_name': patient_name,
            'visit_status': visit_status
        })
    except Exception as e:
        return Response({'error': str(e)}, status=500)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def call_next_patient(request):
    try:
        doctor = request.user.doctor
        today = timezone.localtime().date()
        queue, _ = DailyQueue.objects.get_or_create(doctor=doctor, date=today)

        # 1. Complete Previous Patient (if any)
        if queue.current_token > 0:
            prev_appt = Appointment.objects.filter(
                doctor=doctor,
                appointment_date__date=today,
                token_number=queue.current_token
            ).first()
            
            if prev_appt:
                prev_appt.status = 'completed'
                
                # Save notes if provided
                notes = request.data.get('notes')
                report = request.FILES.get('report_file')
                
                if notes:
                    prev_appt.notes = notes
                if report:
                    prev_appt.report_file = report
                    
                prev_appt.save()

        # 2. Advance Queue
        queue.current_token += 1
        queue.save()

        # 3. Check if we have a patient for this new token
        next_appt = Appointment.objects.filter(
            doctor=doctor,
            appointment_date__date=today,
            token_number=queue.current_token
        ).first()
        
        # If no appointment found for this token (e.g. end of list), 
        # usually we just stay on this token but show "No Patient"
        # The frontend handles knowing when to disable 'Next' based on list size, 
        # but here we just process the token.

        data = {
            'success': True,
            'message': f'Called Token #{queue.current_token}',
            'current_token': queue.current_token,
            'patient_name': next_appt.patient_name if next_appt else None
        }
        return Response(data)

    except Exception as e:
        return Response({'success': False, 'message': str(e)}, status=500)
