import os
import django
from django.utils import timezone
from django.conf import settings

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'revana_hms.settings')
django.setup()

from appointments.models import Appointment
from doctors.models import Doctor

print(f"Server Timezone: {settings.TIME_ZONE}")
print(f"Current Time (now): {timezone.now()}")
print(f"Current Date (local date): {timezone.localdate()}")

today = timezone.now().date()
print(f"Filter Date: {today}")

count = Appointment.objects.filter(appointment_date__date=today).count()
print(f"Total Appointments for {today}: {count}")

# Check sample if any exist
if count > 0:
    appt = Appointment.objects.filter(appointment_date__date=today).first()
    print(f"Sample stored date: {appt.appointment_date}")
else:
    print("No appointments found for today.")
    # Check if there are ANY appointments to see if date format is weird
    last = Appointment.objects.last()
    if last:
        print(f"Latest appointment in DB: {last.appointment_date}")
