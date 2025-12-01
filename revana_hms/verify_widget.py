import os
import django
import json
from datetime import date, time, datetime

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'revana_hms.settings')
django.setup()

from django.test import RequestFactory
from django.contrib.auth import get_user_model
from hospitals.models import Hospital, Department
from doctors.models import Doctor
from appointments.models import DoctorAvailability, Appointment, Patient
from appointments.widget_views import book_appointment_widget

User = get_user_model()

def run_test():
    print("Setting up test data...")
    # Clean up
    Appointment.objects.all().delete()
    DoctorAvailability.objects.all().delete()
    # Don't delete users/hospitals to avoid breaking other things, just get or create
    
    hospital, _ = Hospital.objects.get_or_create(
        name="Test Hospital",
        defaults={
            'registration_number': 'TEST1234',
            'email': 'test@hospital.com',
            'city': 'Test City'
        }
    )
    
    doctor_user, _ = User.objects.get_or_create(email="dr.test@example.com", defaults={'role': 'doctor'})
    doctor, _ = Doctor.objects.get_or_create(
        user=doctor_user,
        defaults={'name': 'Dr. Test', 'hospital': hospital, 'specialization': 'General'}
    )
    
    # Create Availability
    slot = DoctorAvailability.objects.create(
        doctor=doctor, # Corrected: Pass Doctor instance, not User
        date=date.today(),
        start_time=time(10, 0),
        end_time=time(10, 30),
        is_available=True
    )
    
    print(f"Created slot: {slot.id}")
    
    # Test Booking
    data = {
        'full_name': 'Test Patient',
        'email': 'patient.test@example.com',
        'contact_number': '1234567890',
        'slot_id': slot.id
    }
    
    factory = RequestFactory()
    request = factory.post(
        '/appointments/widget/book/',
        data=json.dumps(data),
        content_type='application/json'
    )
    
    print("Calling book_appointment_widget...")
    response = book_appointment_widget(request)
    print(f"Response status: {response.status_code}")
    print(f"Response content: {response.content.decode()}")
    
    if response.status_code == 200:
        resp_data = json.loads(response.content)
        token = resp_data.get('token_number')
        print(f"Token Generated: {token}")
        
        # Verify Database
        appt = Appointment.objects.get(id=resp_data['appointment_id'])
        print(f"Appointment Created: {appt.token_number} == {token}")
        
        patient_user = User.objects.get(email='patient.test@example.com')
        patient = Patient.objects.get(user=patient_user)
        print(f"Patient Created: {patient.name} linked to {patient_user.email}")
        
        # Verify Slot
        slot.refresh_from_db()
        print(f"Slot Available: {slot.is_available}")
        
        if token == 1 and not slot.is_available:
            print("✅ TEST PASSED")
        else:
            print("❌ TEST FAILED")
            
    else:
        print("❌ TEST FAILED: API Error")

if __name__ == "__main__":
    try:
        run_test()
    except Exception as e:
        print(f"❌ TEST FAILED with Exception: {e}")
