import os
import django
import random
from django.utils import timezone
from datetime import timedelta

# Setup Django Environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'revana_hms.settings')
django.setup()

from patients.models import Patient
from hospitals.models import Hospital
from doctors.models import Doctor
from appointments.models import Appointment

def assign_patients():
    
    # 1. Assign Unassigned Patients to Hospitals
    unassigned_patients = Patient.objects.filter(hospital__isnull=True)
    if unassigned_patients.exists():
        print(f"Found {unassigned_patients.count()} unassigned patients. Assigning them to hospitals...")
        hospitals = list(Hospital.objects.filter(status=Hospital.STATUS_APPROVED))
        
        if not hospitals:
            print("No approved hospitals found! Cannot assign.")
            return

        for patient in unassigned_patients:
            hospital = random.choice(hospitals)
            patient.hospital = hospital
            patient.save()
            print(f"Assigned {patient.name} -> {hospital.name}")
    else:
        print("All patients are already assigned to hospitals.")

    # 2. Ensure every patient has at least one appointment (Doctor Assignment)
    # We define "Assigned to Doctor" as having a history with them.
    all_patients = Patient.objects.all()
    print(f"Checking appointments for {all_patients.count()} patients...")

    for patient in all_patients:
        # Check if patient has any appointment linked to their email or name
        # Note: Appointment model uses patient_name/email strings, not FK to Patient model directly 
        # (Based on provided model snippet). 
        # But for this test data, we will match by name/email just to populate DB.
        
        has_appointment = Appointment.objects.filter(patient_email=patient.user.email).exists()
        
        if not has_appointment:
            hospital = patient.hospital
            if not hospital:
                print(f"Skipping {patient.name} (No Hospital)")
                continue

            # Pick a doctor from this hospital
            doctors = hospital.doctor_set.all()
            if not doctors.exists():
                print(f"Skipping {patient.name} (No doctors in {hospital.name})")
                continue
            
            doctor = random.choice(doctors)
            
            # Create a past appointment
            Appointment.objects.create(
                hospital=hospital,
                doctor=doctor,
                patient_name=patient.name,
                patient_email=patient.user.email,
                appointment_date=timezone.now() - timedelta(days=random.randint(1, 30)),
                token_number=random.randint(1, 20),
                status='completed',
                notes="Initial checkup (System Generated)"
            )
            print(f"Created appointment: {patient.name} -> {doctor.name}")

    print("Patient assignment update complete.")

if __name__ == "__main__":
    assign_patients()
