import os
import django
import json
from django.test import RequestFactory

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'revana_hms.settings')
django.setup()

from doctors.models import Doctor
from doctors.monthly_views import create_monthly_availability

# Get Doctor
doctor = Doctor.objects.first()
print(f"Testing with Doctor: {doctor.user.email}")

# Create Request
factory = RequestFactory()
data = {
    "dates": ["2026-01-20"],
    "slots": [{"start_time": "09:00", "end_time": "17:00"}],
    "duration": "30"
}
request = factory.post(
    '/doctors/availability/monthly/',
    data=json.dumps(data),
    content_type='application/json'
)
request.user = doctor.user

# Call View
response = create_monthly_availability(request)
print(f"Response Status: {response.status_code}")
print(f"Response Body: {response.content.decode('utf-8')}")
