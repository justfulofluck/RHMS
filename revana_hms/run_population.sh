#!/bin/bash

# Simple wrapper to run population with feedback
echo "🚀 Starting HMS Demo Data Population"
echo "======================================"

# Check if we're in right place
if [ ! -f "manage.py" ]; then
    echo "❌ Error: Please run from Django project root (where manage.py exists)"
    exit 1
fi

echo "✓ Found manage.py - in correct directory"
echo "✓ Step 1: Creating hospitals, doctors, patients..."
python3 populate_test_data.py

echo "✓ Step 2: Creating patient appointments..."
python3 assign_patients.py

echo "======================================"
echo "✅ Data population complete!"
echo ""
echo "📊 Quick Summary:"
python3 -c "
import os, django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'revana_hms.settings')
django.setup()
from django.contrib.auth import get_user_model
from hospitals.models import Hospital, HospitalAdmin
from doctors.models import Doctor
from patients.models import Patient
from appointments.models import Appointment
User = get_user_model()
print(f'   🏥 Hospitals: {Hospital.objects.count()}')
print(f'   👨‍⚕️  Doctors: {Doctor.objects.count()}')
print(f'   👥 Patients: {Patient.objects.count()}')
print(f'   📅 Appointments: {Appointment.objects.count()}')
print(f'   👤 Hospital Admins: {User.objects.filter(role=\"hospital_admin\").count()}')
"
echo ""
echo "🔑 All user passwords: password123"
echo "🌐 Run: python3 manage.py runserver to start testing"
echo ""