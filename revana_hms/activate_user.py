import os
import django
import sys

# Setup Django environment
sys.path.append('/home/bhavan/Desktop/RHMS/revana_hms')
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'revana_hms.settings')
django.setup()

from django.contrib.auth import get_user_model
from hospitals.models import HospitalAdmin

User = get_user_model()

try:
    user = User.objects.get(email='bhavanbadhe@gmail.com')
    print(f"User found: {user.email} (ID: {user.id})")
    print(f"Current Status - Role: {user.role}, Active: {user.is_active}")
    
    if not user.is_active:
        print("Activating user...")
        user.is_active = True
        user.save()
        print("User activated.")
    else:
        print("User is already active.")
        
    # Verify HospitalAdmin link
    try:
        ha = HospitalAdmin.objects.get(user=user)
        print(f"Linked HospitalAdmin: ID {ha.id}, Hospital: {ha.hospital.name}")
    except HospitalAdmin.DoesNotExist:
        print("ERROR: No HospitalAdmin linked to this user!")

except User.DoesNotExist:
    print("User bhavanbadhe@gmail.com not found.")
