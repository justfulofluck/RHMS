
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
    print("Listing last 10 appointments in the database (by ID desc):")
    print("-" * 100)
    
    appts = Appointment.objects.all().order_by('-id')[:10]
    
    if not appts.exists():
        print("No appointments found in database.")
        return

    print(f"{'ID':<5} | {'Date':<22} | {'Patient Name':<20} | {'Doctor':<20} | {'Patient Email'}")
    print("-" * 100)

    for appt in appts:
        print(f"{appt.id:<5} | {str(appt.appointment_date):<22} | {appt.patient_name[:19]:<20} | {appt.doctor.name if appt.doctor else 'None':<20} | {appt.patient_email}")

    print("-" * 100)
    print(f"Total Appointments in DB: {Appointment.objects.count()}")

if __name__ == "__main__":
    debug_data()


if __name__ == "__main__":
    debug_data()
