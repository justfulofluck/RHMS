from django.http import JsonResponse
from django.views.decorators.http import require_GET, require_POST
from django.views.decorators.csrf import csrf_exempt
from django.utils import timezone
from django.conf import settings
from django.db import transaction
from django.core.mail import send_mail
from django.contrib.auth import get_user_model

from hospitals.models import Hospital, Department
from doctors.models import Doctor
from appointments.models import Appointment, DoctorAvailability
from patients.models import Patient

import json
from datetime import datetime

User = get_user_model()

@require_GET
def get_cities(request):
    # Only show cities with approved hospitals
    cities = Hospital.objects.filter(status=Hospital.STATUS_APPROVED).values_list('city', flat=True).distinct()
    return JsonResponse({'cities': list(cities)})

@require_GET
def get_departments(request):
    city = request.GET.get('city')
    if not city:
        return JsonResponse({'error': 'City is required'}, status=400)
    
    # Only show departments from approved hospitals
    departments = Department.objects.filter(
        hospital__city=city,
        hospital__status=Hospital.STATUS_APPROVED
    ).values_list('name', flat=True).distinct()
    return JsonResponse({'departments': list(departments)})

@require_GET
def get_hospitals(request):
    city = request.GET.get('city')
    department = request.GET.get('department')
    
    if not city or not department:
        return JsonResponse({'error': 'City and Department are required'}, status=400)
    
    # Only show approved hospitals
    hospitals = Hospital.objects.filter(
        city=city, 
        departments__name=department,
        status=Hospital.STATUS_APPROVED  # ✅ Only approved hospitals
    ).values('id', 'name').distinct()
    
    return JsonResponse({'hospitals': list(hospitals)})

@require_GET
def get_doctors(request):
    hospital_id = request.GET.get('hospital_id')
    department = request.GET.get('department')
    
    if not hospital_id or not department:
        return JsonResponse({'error': 'Hospital ID and Department are required'}, status=400)
    
    # Only show doctors from approved hospitals AND approved doctors
    doctors = Doctor.objects.filter(
        hospital_id=hospital_id,
        hospital__status=Hospital.STATUS_APPROVED,  # ✅ Only approved hospitals
        status=Doctor.STATUS_APPROVED,  # ✅ Only approved doctors
        department__name=department
    ).values('id', 'name', 'specialization')
    
    return JsonResponse({'doctors': list(doctors)})

@require_GET
def get_slots(request):
    """Get available time slots for a doctor - returns individual slots based on duration"""
    from appointments.utils import generate_time_slots
    
    doctor_id = request.GET.get('doctor_id')
    if not doctor_id:
        return JsonResponse({'error': 'Doctor ID is required'}, status=400)
    
    today = timezone.now().date()
    availabilities = DoctorAvailability.objects.filter(
        doctor_id=doctor_id,
        date__gte=today,
        is_available=True
    ).order_by('date', 'start_time')
    
    # Generate individual slots from availabilities
    all_slots = []
    for availability in availabilities:
        individual_slots = generate_time_slots(availability)
        all_slots.extend(individual_slots)
    
    # Format for JSON response
    data = []
    for idx, slot in enumerate(all_slots):
        # Create unique ID combining availability ID and slot index
        slot_id = f"{slot['availability_id']}_{idx}"
        data.append({
            'id': slot_id,
            'date': slot['date'].strftime('%Y-%m-%d'),
            'start_time': slot['start_time'].strftime('%H:%M'),
            'end_time': slot['end_time'].strftime('%H:%M'),
            'duration': slot['duration']
        })
        
    return JsonResponse({'slots': data})

@csrf_exempt
@require_POST
def book_appointment_widget(request):
    """Book appointment using individual time slot"""
    from appointments.utils import generate_time_slots
    
    try:
        data = json.loads(request.body)
        
        # Extract data
        full_name = data.get('full_name')
        email = data.get('email')
        contact_number = data.get('contact_number')
        slot_id = data.get('slot_id')  # Format: "availability_id_slot_index"
        
        if not all([full_name, email, contact_number, slot_id]):
            return JsonResponse({'error': 'Missing required fields'}, status=400)
        
        # Parse slot ID to get availability ID and slot index
        try:
            availability_id, slot_index = slot_id.split('_')
            availability_id = int(availability_id)
            slot_index = int(slot_index)
        except (ValueError, AttributeError):
            return JsonResponse({'error': 'Invalid slot ID format'}, status=400)
            
        with transaction.atomic():
            # 1. Get Availability and generate slots
            try:
                availability = DoctorAvailability.objects.select_for_update().get(
                    id=availability_id,
                    is_available=True
                )
            except DoctorAvailability.DoesNotExist:
                return JsonResponse({'error': 'Slot not available'}, status=400)
            
            # Generate individual slots from this availability
            individual_slots = generate_time_slots(availability)
            
            # Get the specific slot the patient selected
            if slot_index >= len(individual_slots):
                return JsonResponse({'error': 'Invalid slot index'}, status=400)
            
            selected_slot = individual_slots[slot_index]
            
            # 2. User Registration / Retrieval
            user, created = User.objects.get_or_create(email=email, defaults={
                'role': 'patient',
                'is_active': True
            })
            if created:
                user.set_unusable_password() # User needs to reset password or login via magic link
                user.save()
                
            # 3. Patient Profile
            patient, _ = Patient.objects.get_or_create(user=user, defaults={
                'age': 0, # Default, user should update
                'gender': 'Other', # Default
                'phone': contact_number,
                'address': ''
            })
            
            # 4. Token Generation
            appointment_date = selected_slot['date']
            hospital = availability.doctor.hospital
            
            # Count appointments for this hospital on this date to generate token
            current_count = Appointment.objects.filter(
                hospital=hospital,
                appointment_date__date=appointment_date
            ).count()
            
            token_number = current_count + 1
            if token_number > 500:
                return JsonResponse({'error': 'Daily token limit reached for this hospital'}, status=400)
            
            # 5. Create Appointment with specific start time
            from datetime import datetime
            appointment_start = datetime.combine(
                selected_slot['date'],
                selected_slot['start_time']
            )
            
            appointment = Appointment.objects.create(
                hospital=hospital,
                doctor=availability.doctor,
                patient_name=full_name,
                appointment_date=appointment_start,
                token_number=token_number,
                created_at=timezone.now()
            )
            
            # 6. Mark Slot Unavailable (simplified - marks entire availability)
            # TODO: Track individual slot bookings for better granularity
            # For now, we'll leave availability as is since we're tracking appointments
            
            # 7. Send Email
            from appointments.utils import format_time_12hr
            subject = f"Appointment Confirmed - Token #{token_number}"
            message = f"""
            Dear {full_name},
            
            Your appointment has been confirmed.
            
            Doctor: {availability.doctor.name}
            Hospital: {hospital.name}
            Date: {selected_slot['date'].strftime('%B %d, %Y')}
            Time: {format_time_12hr(selected_slot['start_time'])} - {format_time_12hr(selected_slot['end_time'])}
            Duration: {selected_slot['duration']} minutes
            Token Number: {token_number}
            
            Please arrive 10 minutes before your appointment time.
            
            Thank you for choosing us.
            """
            try:
                send_mail(subject, message, settings.DEFAULT_FROM_EMAIL, [email])
            except Exception as e:
                print(f"Email sending failed: {e}") # Non-blocking
            
            return JsonResponse({
                'success': True,
                'message': 'Appointment booked successfully',
                'token_number': token_number,
                'appointment_id': appointment.id,
                'start_time': format_time_12hr(selected_slot['start_time']),
                'end_time': format_time_12hr(selected_slot['end_time']),
                'duration': selected_slot['duration']
            })

    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)
