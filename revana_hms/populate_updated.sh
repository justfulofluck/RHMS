#!/bin/bash

# HMS Demo Data Population Script - Updated Version
# Handles existing data and provides options to clear or proceed

set -e  # Exit on any error

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
CYAN='\033[0;36m'
NC='\033[0m' # No Color

# Print colored output
print_status() {
    echo -e "${BLUE}[INFO]${NC} $1"
}

print_success() {
    echo -e "${GREEN}[SUCCESS]${NC} $1"
}

print_warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
}

print_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

print_header() {
    echo -e "${CYAN}=== $1 ===${NC}"
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

print_header "HMS Demo Data Population Script"

# Function to check existing data
check_existing_data() {
    print_status "Checking existing data..."
    
    python3 -c "
import os
import django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'revana_hms.settings')
django.setup()

from django.contrib.auth import get_user_model
from hospitals.models import Hospital
from doctors.models import Doctor
from patients.models import Patient
from appointments.models import Appointment

User = get_user_model()

hospitals = Hospital.objects.count()
users = User.objects.count()
doctors = Doctor.objects.count()
patients = Patient.objects.count()
appointments = Appointment.objects.count()

print(f'EXISTS - Hospitals: {hospitals}, Users: {users}, Doctors: {doctors}, Patients: {patients}, Appointments: {appointments}')

if hospitals > 0 or users > 0 or doctors > 0 or patients > 0 or appointments > 0:
    print('HAS_DATA')
else:
    print('CLEAN')
" 2>/dev/null | grep -q "HAS_DATA"
}

# Function to clear database safely
clear_database() {
    print_status "Clearing existing data..."
    print_warning "This will delete ALL existing data from the database!"
    
    # Try different approaches to flush database
    if python3 manage.py flush --no-input 2>/dev/null; then
        print_success "Database cleared successfully"
    elif echo "yes" | python3 manage.py flush 2>/dev/null; then
        print_success "Database cleared successfully"
    else
        print_error "Failed to clear database. You may need to clear manually:"
        print_status "Run: python3 manage.py shell"
        print_status "Then: from django.db import connection; connection.cursor().execute('DELETE FROM auth_user;')"
        exit 1
    fi
}

# Function to run script with progress tracking
run_script() {
    local script_name=$1
    local description=$2
    
    print_status "Running $script_name - $description..."
    
    # Run with progress indication
    start_time=$(date +%s)
    
    if python3 "$script_name"; then
        end_time=$(date +%s)
        duration=$((end_time - start_time))
        print_success "$script_name completed successfully in ${duration}s"
        return 0
    else
        print_error "$script_name failed"
        return 1
    fi
}

# Function to generate final summary
generate_summary() {
    print_status "Generating final summary..."
    
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

print('📊 FINAL DATA SUMMARY')
print('=' * 50)

# Totals
total_hospitals = Hospital.objects.count()
total_admins = HospitalAdmin.objects.count()
total_doctors = Doctor.objects.count()
total_patients = Patient.objects.count()
total_appointments = Appointment.objects.count()

print(f'🏥  Total Hospitals: {total_hospitals}')
print(f'👨‍⚕️  Total Hospital Admins: {total_admins}')
print(f'👨‍⚕️  Total Doctors: {total_doctors}')
print(f'👥 Total Patients: {total_patients}')
print(f'📅 Total Appointments: {total_appointments}')
print('')

# User breakdown
admin_users = User.objects.filter(role='hospital_admin').count()
doctor_users = User.objects.filter(role='doctor').count()
patient_users = User.objects.filter(role='patient').count()

print('👤 USER BREAKDOWN:')
print(f'  • Hospital Admins: {admin_users}')
print(f'  • Doctors: {doctor_users}')
print(f'  • Patients: {patient_users}')
print(f'  • Total Users: {admin_users + doctor_users + patient_users}')
print('')

# Hospital distribution (show detailed breakdown)
print('🏥 HOSPITAL DISTRIBUTION:')
hospitals = Hospital.objects.all()
if hospitals.exists():
    for i, hospital in enumerate(hospitals, 1):
        doctor_count = Doctor.objects.filter(hospital=hospital).count()
        patient_count = Patient.objects.filter(hospital=hospital).count()
        print(f'  {i:2d}. {hospital.name[:30]:<30}: {doctor_count:2d} doctors, {patient_count:2d} patients')
else:
    print('  No hospitals found')
print('=' * 50)

# Check for issues
if total_patients == 0:
    print_warning('No patients created - check populate_test_data.py')
if total_doctors == 0:
    print_warning('No doctors created - check populate_test_data.py')
if total_appointments == 0:
    print_warning('No appointments created - check assign_patients.py')
if total_doctors > 0 and total_patients > 0 and total_appointments == 0:
    print_warning('Doctors and patients exist but no appointments - run assign_patients.py')

if total_hospitals == 10 and total_doctors == 50 and total_patients == 60:
    print_success('✅ Perfect distribution achieved! (10 hospitals, 50 doctors, 60 patients)')
    print_success('✅ All scripts completed successfully!')
else:
    print_warning('⚠️  Data distribution differs from expected')
    print_status('Expected: 10 hospitals, 50 doctors, 60 patients')
" 2>/dev/null || print_warning "Could not generate detailed summary"
}

# Main execution logic
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

# Check existing data
print_header "Existing Data Check"
if check_existing_data; then
    print_warning "Existing data found in database!"
    print ""
    echo "Options:"
    echo "1) Clear all data and populate fresh (recommended)"
    echo "2) Add to existing data (may cause duplicates)"
    echo "3) Exit and handle manually"
    echo ""
    read -p "Choose option (1-3): " choice
    
    case $choice in
        1)
            clear_database
            ;;
        2)
            print_warning "Proceeding with existing data (may cause conflicts)..."
            ;;
        3)
            print_status "Exiting. Please handle data manually."
            exit 0
            ;;
        *)
            print_error "Invalid option. Exiting."
            exit 1
            ;;
    esac
else
    print_success "Database is clean - proceeding with population"
fi

# Main population
print_header "Data Population"
echo ""

# Step 1: Create base entities
run_script "populate_test_data.py" "Creating hospitals, doctors, and patients with equal distribution"

echo ""

# Step 2: Create relationships
run_script "assign_patients.py" "Creating patient-doctor appointments"

echo ""

print_header "Population Complete"
echo ""

# Generate comprehensive summary
generate_summary

echo ""
print_success "🎉 All operations completed!"
print_status "You can now test HMS system with demo data."
print_status "Run: python3 manage.py runserver to start testing."
print_status "Login credentials: All users have password 'password123'"

echo ""
print_header "Quick Test Commands"
echo "• Start server: python3 manage.py runserver"
echo "• Access admin: http://127.0.0.1:8000/admin/"
echo "• Test with users from the summary above"

exit 0