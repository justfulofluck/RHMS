
import os
import django
from django.conf import settings

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'revana_hms.settings')
django.setup()

from django.test import Client
from django.contrib.auth import get_user_model
from doctors.models import Doctor

User = get_user_model()

def verify():
    # Find a doctor
    doctor = Doctor.objects.first()
    if not doctor:
        print("No doctor found to test with.")
        return

    print(f"Testing with doctor: {doctor.user.email}")

    c = Client()
    c.force_login(doctor.user)

    response = c.get('/hospital/doctors/dashboard/')
    
    if response.status_code != 200:
        print(f"Failed to get dashboard. Status: {response.status_code}")
        return

    content = response.content.decode('utf-8')
    
    if "Contact" in content and "Patient Name" in content:
        print("SUCCESS: 'Contact' column found in dashboard.")
    else:
        print("FAILURE: 'Contact' column NOT found in dashboard.")

    # Check for phone number if appointments exist
    if "9999999999" in content: # assuming dummy data might have this, or just checking column is enough
        pass 

if __name__ == "__main__":
    verify()
