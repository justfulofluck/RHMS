import os
import django
from django.utils import timezone

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'revana_hms.settings')
django.setup()

from appointments.models import Appointment
from doctors.models import Doctor

def fix_tokens():
    today = timezone.localtime().date()
    print(f"--- Fixing Tokens for {today} ---")
    
    # Get all appointments for today, ordered by creation time (so first booked gets #1)
    appointments = Appointment.objects.filter(
        appointment_date__date=today
    ).order_by('created_at')
    
    token_counter = 1
    for app in appointments:
        old_token = app.token_number
        app.token_number = token_counter
        app.save()
        print(f"Updates {app.patient_name}: Token {old_token} -> {app.token_number}")
        token_counter += 1
        
    print("Tokens re-sequenced successfully.")

if __name__ == "__main__":
    fix_tokens()
