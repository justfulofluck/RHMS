import os
import django
from django.utils import timezone

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'revana_hms.settings')
django.setup()

from appointments.models import Appointment, DailyQueue
from doctors.models import Doctor

def debug_queue():
    today = timezone.localtime().date()
    print(f"--- Debugging for Date: {today} ---")

    # 1. Inspect Queues
    queues = DailyQueue.objects.filter(date=today)
    for q in queues:
        print(f"Queue for {q.doctor.name}: Current Token = {q.current_token}")

    # 2. Inspect Appointments
    appointments = Appointment.objects.filter(appointment_date__date=today).order_by('token_number')
    print(f"\n--- Appointments ({appointments.count()}) ---")
    for app in appointments:
        print(f"[{app.status}] Token #{app.token_number}: {app.patient_name} (Doctor: {app.doctor.name})")
        # Reset Status
        app.status = 'scheduled'
        app.save()
        print(f" -> Reset {app.patient_name} to 'scheduled'")

    # 3. Fix?
    # Uncomment to reset queue
    for q in queues:
        q.current_token = 0
        q.save()
        print(f"RESET queue for {q.doctor.name} to 0")

if __name__ == "__main__":
    debug_queue()
