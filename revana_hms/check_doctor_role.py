import os
import django
from django.conf import settings

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'revana_hms.settings')
django.setup()

from accounts.models import User
from doctors.models import Doctor

last_doctor = Doctor.objects.last()
if last_doctor:
    u = last_doctor.user
    print(f"Doctor User: {u.email} (ID: {u.id})")
    print(f"Role: '{u.role}'")
    print(f"Is Active: {u.is_active}")
    print(f"Is Superuser: {u.is_superuser}")
else:
    print("No doctors found.")
