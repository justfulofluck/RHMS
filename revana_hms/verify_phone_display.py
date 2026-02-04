
import os
import django
from django.conf import settings
from django.utils import timezone
from datetime import timedelta

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'revana_hms.settings')
django.setup()

from django.test import Client
from django.contrib.auth import get_user_model
from doctors.models import Doctor
from appointments.models import Appointment
from patients.models import Patient
from hospitals.models import Hospital

User = get_user_model()

def verify():
    # Find a doctor
    doctor = Doctor.objects.first()
    if not doctor:
        print("No doctor found to test with.")
        return

    print(f"Testing with doctor: {doctor.user.email}")

    # Create Test Data
    created_data = False
    test_email = "test_patient_verify@example.com"
    test_phone = "1234567890"
    
    # 1. Ensure Patient Exists
    try:
        user = User.objects.get(email=test_email)
        patient = Patient.objects.get(user=user)
    except User.DoesNotExist:
        user = User.objects.create_user(email=test_email, password="password123", role="patient")
        patient = Patient.objects.create(
            user=user, 
            phone=test_phone, 
            age=30, 
            gender="Male", 
            name="Test Verification Patient"
        )
        created_data = True
        print("Created test patient.")

    # 2. Ensure Appointment Exists for Today
    today = timezone.localdate()
    appt_time = timezone.now().replace(hour=10, minute=0, second=0, microsecond=0)
    
    appt = Appointment.objects.filter(
        doctor=doctor, 
        patient_email=test_email,
        appointment_date__date=today
    ).first()

    if not appt:
        appt = Appointment.objects.create(
            doctor=doctor,
            patient_name=patient.name,
            patient_email=patient.user.email,
            appointment_date=appt_time,
            status='scheduled',
            hospital=doctor.hospital,
            token_number=999
        )
        created_data = True
        print("Created test appointment.")

    # --- VERIFICATION ---
    print(f"Checking for Patient: {patient.name}")
    print(f"Expected Phone Number: {patient.phone}")

    c = Client()
    c.force_login(doctor.user)

    response = c.get('/hospital/doctors/dashboard/')
    
    if response.status_code != 200:
        print(f"Failed to get dashboard. Status: {response.status_code}")
        return

    content = response.content.decode('utf-8')
    
    if "Contact" in content:
        print("SUCCESS: 'Contact' column found in dashboard.")
    else:
        print("FAILURE: 'Contact' column NOT found in dashboard.")
    
    if str(patient.phone) in content:
        print(f"SUCCESS: Phone number {patient.phone} found in dashboard HTML.")
    else:
        print(f"FAILURE: Phone number {patient.phone} NOT found in dashboard HTML.")
        # Debug: print snippet of content
        # print(content[:1000])

    # --- CLEANUP ---
    if created_data:
        print("Cleaning up test data...")
        appt.delete()
        if user.email == test_email:
             patient.delete()
             user.delete()
        print("Cleanup complete.")

if __name__ == "__main__":
    verify()
