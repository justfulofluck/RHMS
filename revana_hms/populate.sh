#!/bin/bash

# HMS Demo Data Population Script
# Runs populate_test_data.py and assign_patients.py in proper order

set -e  # Exit on any error

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Print colored output
print_status() {
    echo -e "${BLUE}[INFO]${NC} $1"
}

print_success() {
    echo -e "${GREEN}[SUCCESS]${NC} $1"
}

print_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

print_warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
}

# Check if we're in right directory
if [ ! -f "manage.py" ]; then
    print_error "manage.py not found. Please run this script from Django project root directory."
    exit 1
fi

# Check if Python is available
if ! command -v python3 &> /dev/null; then
    print_error "python3 not found. Please install Python 3."
    exit 1
fi

print_status "Checking Django environment..."
python3 -c "
import os
import django
try:
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'revana_hms.settings')
    django.setup()
    print('✓ Django setup successful')
except Exception as e:
    print(f'✗ Django setup failed: {e}')
    exit(1)
"

print_success "Django environment OK"

# Function to run script with error handling
run_script() {
    local script_name=$1
    local description=$2
    
    print_status "Running $script_name - $description..."
    
    if python3 "$script_name"; then
        print_success "$script_name completed successfully"
        return 0
    else
        print_error "$script_name failed"
        return 1
    fi
}

# Main execution
print_status "Starting HMS Demo Data Population"
echo "================================================"

# Step 1: Create base entities
run_script "populate_test_data.py" "Creating hospitals, doctors, and patients with equal distribution"

# Step 2: Create patient-doctor relationships
run_script "assign_patients.py" "Creating patient-doctor appointments"

echo "================================================"

# Display summary
print_status "Generating data summary..."
python3 -c "
import os
import django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'revana_hms.settings')
django.setup()

from django.contrib.auth import get_user_model
from hospitals.models import Hospital, HospitalAdmin
from doctors.models import Doctor
from patients.models import Patient
from appointments.models import Appointment

User = get_user_model()

print('📊 DATA POPULATION SUMMARY')
print('=' * 40)
print(f'🏥 Hospitals: {Hospital.objects.count()}')
print(f'👨‍⚕️  Hospital Admins: {HospitalAdmin.objects.count()}')
print(f'👨‍⚕️  Doctors: {Doctor.objects.count()}')
print(f'👥 Patients: {Patient.objects.count()}')
print(f'📅 Appointments: {Appointment.objects.count()}')
print('')
print('👤 USER BREAKDOWN:')
print(f'  • Hospital Admins: {User.objects.filter(role=\"hospital_admin\").count()}')
print(f'  • Doctors: {User.objects.filter(role=\"doctor\").count()}')
print(f'  • Patients: {User.objects.filter(role=\"patient\").count()}')
print('')

# Hospital distribution (show first 10)
print('🏥 HOSPITAL DISTRIBUTION (showing first 10):')
for hospital in Hospital.objects.all()[:10]:
    doctor_count = Doctor.objects.filter(hospital=hospital).count()
    patient_count = Patient.objects.filter(hospital=hospital).count()
    print(f'  • {hospital.name[:25]:<25}: {doctor_count} doctors, {patient_count} patients')
print('=' * 40)
" || print_warning "Could not generate detailed summary"

if [ $? -eq 0 ]; then
    print_success "Data population completed successfully! 🚀"
    print_status "You can now test the HMS system with demo data."
    print_status "Run: python3 manage.py runserver to start testing."
else
    print_error "Data population had issues. Check the error messages above."
fi

exit 0