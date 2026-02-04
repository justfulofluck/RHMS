
import os
import django
from django.conf import settings
from django.utils import timezone

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'revana_hms.settings')
django.setup()

from doctors.models import Doctor
from appointments.models import Appointment
from patients.models import Patient


def debug_data():
    # Find the doctor who has appointments with 'bhavanbadhe12' or 'Dharmik'
    target_patient_name = "bhavanbadhe12"
    
    today = timezone.localdate()
    
    # Try to find an appointment with this patient
    sample_appt = Appointment.objects.filter(
        patient_name__icontains=target_patient_name,
        appointment_date__date=today
    ).first()

    if not sample_appt:
        print(f"Could not find any appointments today for patient '{target_patient_name}'.")
        print("Trying 'Dharmik'...")
        sample_appt = Appointment.objects.filter(
            patient_name__icontains="Dharmik",
            appointment_date__date=today
        ).first()

    if not sample_appt:
         print("No appointments found for either patient. Listing ALL appointments for today...")
         appts = Appointment.objects.filter(appointment_date__date=today)
         if not appts.exists():
             print("Create NO appointments found for today in the entire DB.")
             return
         else:
             print(f"Found {appts.count()} total appointments today.")
             doctor = appts.first().doctor # Pick the first one
    else:
        doctor = sample_appt.doctor
        print(f"Identified Doctor: {doctor.name} ({doctor.user.email}) from appointment with {sample_appt.patient_name}")

    if not doctor:
        print("No doctor found.")
        return

    print(f"Checking appointments for doctor: {doctor.user.email}")
    
    appointments = Appointment.objects.filter(
        doctor=doctor,
        appointment_date__date=today
    ).order_by('appointment_date')

    print(f"Found {appointments.count()} appointments for today.")
    print("-" * 60)
    print(f"{'Patient Name':<20} | {'Email':<30} | {'Found User?':<12} | {'Found Patient?':<15} | {'Phone'}")
    print("-" * 60)

    for appt in appointments:
        email = appt.patient_email
        found_user = "No"
        found_patient = "No"
        phone = "-"
        
        if email:
            try:
                # 1. Check if Patient exists by email
                patient = Patient.objects.filter(user__email=email).first()
                if patient:
                    found_user = "Yes"
                    found_patient = "Yes"
                    phone = patient.phone
                else:
                    # 2. Check if User exists but no Patient profile
                    from django.contrib.auth import get_user_model
                    User = get_user_model()
                    user = User.objects.filter(email=email).first()
                    if user:
                        found_user = "Yes (No Profile)"
                    
            except Exception as e:
                found_patient = f"Error: {e}"

        print(f"{appt.patient_name[:19]:<20} | {str(email)[:29]:<30} | {found_user:<12} | {found_patient:<15} | {phone}")

if __name__ == "__main__":
    debug_data()
