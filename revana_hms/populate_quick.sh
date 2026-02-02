#!/bin/bash

# Minimal HMS Demo Data Population Script
# Simplified version with timeout handling and progress tracking

set -e

# Colors
GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
NC='\033[0m'

print_info() {
    echo -e "${BLUE}[INFO]${NC} $1"
}

print_success() {
    echo -e "${GREEN}[SUCCESS]${NC} $1"
}

print_warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
}

# Check directory
if [ ! -f "manage.py" ]; then
    echo "Error: Run from Django project root"
    exit 1
fi

print_info "Quick HMS Data Population"
echo "=============================="

# Step 1: Clear database
print_info "Clearing existing data..."
echo "y" | python3 manage.py flush --no-input 2>/dev/null || {
    print_warning "Manual database clear may be needed"
}

# Step 2: Run populate script with progress
print_info "Running populate_test_data.py..."
print_info "This may take 1-2 minutes..."

# Run with timeout and background process handling
timeout 180 python3 populate_test_data.py || {
    print_warning "Population timed out or failed"
    print_info "Checking partial data..."
    
    # Check what was created
    python3 -c "
import os, django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'revana_hms.settings')
django.setup()
from hospitals.models import Hospital
from doctors.models import Doctor
from patients.models import Patient
print(f'Created: {Hospital.objects.count()} hospitals, {Doctor.objects.count()} doctors, {Patient.objects.count()} patients')
"
}

# Step 3: Run assignment script
print_info "Running assign_patients.py..."
timeout 60 python3 assign_patients.py || {
    print_warning "Assignment script had issues"
}

# Step 4: Quick summary
print_info "Generating summary..."
python3 -c "
import os, django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'revana_hms.settings')
django.setup()
from django.contrib.auth import get_user_model
from hospitals.models import Hospital
from doctors.models import Doctor
from patients.models import Patient
from appointments.models import Appointment
User = get_user_model()

print('📊 SUMMARY:')
print(f'Hospitals: {Hospital.objects.count()}')
print(f'Doctors: {Doctor.objects.count()}') 
print(f'Patients: {Patient.objects.count()}')
print(f'Appointments: {Appointment.objects.count()}')
print(f'Admins: {User.objects.filter(role=\"hospital_admin\").count()}')
"

print_success "Population script completed!"
print_info "All passwords: password123"
print_info "Run server: python3 manage.py runserver"