# HMS Demo Data Population Guide

## Overview
This directory contains scripts to populate the HMS database with demo data for testing purposes.

## Files

### 1. `populate_test_data.py`
- **Purpose**: Creates base entities (hospitals, doctors, patients) with equal distribution
- **Creates**:
  - 10 hospitals (2 per city: Surat, Ahmedabad, Vadodara, Gandhinagar, Rajkot)
  - 20 hospital admins
  - 50 doctors (5 per hospital - equal distribution)
  - 60 patients (6 per hospital - equal distribution)
  - 3 departments per hospital with treatments
- **Features**:
  - Strict equal distribution for balanced testing
  - All patients assigned to hospitals immediately
  - Uses Indian localization with Faker

### 2. `assign_patients.py`
- **Purpose**: Creates patient-doctor relationships through appointments
- **Creates**:
  - Past appointments for all patients (1-30 days ago)
  - Assigns patients to doctors from their hospital
  - Maintains hospital boundaries in appointments
- **Features**:
  - Smart doctor selection from patient's hospital
  - Avoids hospitals without doctors
  - Creates realistic appointment history

### 3. `populate.sh`
- **Purpose**: Shell script to run both Python scripts in proper order
- **Features**:
  - Environment validation
  - Error handling and colored output
  - Data summary reporting
  - Execution status tracking

## Usage

### Quick Start
```bash
# Make sure the script is executable
chmod +x populate.sh

# Run the complete data population
./populate.sh
```

### Individual Script Execution
```bash
# Create base entities only
python3 populate_test_data.py

# Create appointments only (run after populate_test_data.py)
python3 assign_patients.py
```

## Data Distribution (Equal Distribution)

### Hospitals
- **Total**: 10 hospitals
- **Per City**: 2 hospitals
- **Cities**: Surat, Ahmedabad, Vadodara, Gandhinagar, Rajkot
- **Departments**: 3 per hospital (randomly selected)
- **Treatments**: 2 per department (Consultation, Surgery)

### Staff Distribution
- **Hospital Admins**: 20 (randomly distributed)
- **Doctors**: 50 (5 per hospital - exact)
- **Patients**: 60 (6 per hospital - exact)
- **User Roles**: Proper role assignment (hospital_admin, doctor, patient)

### Relationships
- **Doctor ↔ Hospital**: Direct ForeignKey (balanced)
- **Patient ↔ Hospital**: Direct ForeignKey (guaranteed)
- **Patient ↔ Doctor**: Through Appointment model

## Before Running

### Prerequisites
1. **Python 3+** installed
2. **Django project set up** with database
3. **Required packages**: `faker`, Django
4. **Database migrations applied**: `python3 manage.py migrate`
5. **Run from project root**: Where `manage.py` is located

### Database Check
```bash
# Verify database connection
python3 manage.py check

# Apply migrations if needed
python3 manage.py migrate
```

## Expected Output

### populate_test_data.py
```
Starting data population...
Creating Hospitals...
Created 10 hospitals.
Creating 20 Hospital Admins...
Admins created.
Creating 50 Doctors...
Doctors created.
Creating 60 Patients...
Patients created.
Data population complete! 🚀
```

### assign_patients.py
```
Checking appointments for 60 patients...
Created appointment: Patient Name -> Doctor Name
... (more appointment lines) ...
Patient assignment update complete.
```

### populate.sh Summary
```
📊 DATA POPULATION SUMMARY
========================================
🏥 Hospitals: 10
👨‍⚕️  Hospital Admins: 20
👨‍⚕️  Doctors: 50
👥 Patients: 60
📅 Appointments: ~45-55
👤 USER BREAKDOWN:
  • Hospital Admins: 20
  • Doctors: 50
  • Patients: 60
🏥 HOSPITAL DISTRIBUTION (showing first 10):
  • Hospital Name A                : 5 doctors, 6 patients
  • Hospital Name B                : 5 doctors, 6 patients
  ...
========================================
```

## Benefits of Equal Distribution

### ✅ Advantages
1. **Balanced Testing**: Each hospital gets fair workload
2. **Predictable Results**: Same data distribution every run
3. **Complete Coverage**: No orphaned patients or empty hospitals
4. **Consistent Ratios**: Doctor-patient ratio is controlled
5. **Reliable Testing**: Good for automated test scenarios

### ⚠️ Considerations
1. **Less Realistic**: Real hospitals have uneven distribution
2. **Uniform Load**: Doesn't mirror real-world variability
3. **Perfect Balance**: Natural randomness is removed

## Troubleshooting

### Common Issues
1. **Import Errors**: Check Python path and Django settings
2. **Database Errors**: Verify database connection and migrations
3. **Permission Errors**: Ensure script is executable (`chmod +x`)
4. **Timeout Issues**: Scripts may take time with large datasets

### Debug Mode
Run scripts individually for debugging:
```bash
# Check Django setup
python3 -c "import django; django.setup(); print('Django OK')"

# Test model imports
python3 -c "
from django.contrib.auth import get_user_model
from hospitals.models import Hospital
print('Models OK')
"
```

## Post-Population Testing

### Test Login Credentials
All users have password: `password123`

- **Hospital Admins**: Check their assigned hospitals
- **Doctors**: Verify departments and availability
- **Patients**: Test appointment booking

### Next Steps
1. **Start Development Server**: `python3 manage.py runserver`
2. **Test Login**: Try different user roles
3. **Verify Data**: Check admin panel for data integrity
4. **Run Tests**: Use the demo data for testing features

## Customization

### Changing Numbers
Edit the main execution in `populate_test_data.py`:
```python
create_admins(hospitals, 30)  # Change from 20
create_doctors(hospitals, 100)  # Change from 50
create_patients(hospitals, 120)  # Change from 60
```

### Adding Cities
Update `CITIES` constant:
```python
CITIES = ["Surat", "Ahmedabad", "Vadodara", "Gandhinagar", "Rajkot", "NewCity"]
```

### Modifying Departments
Update `DEPARTMENTS` constant:
```python
DEPARTMENTS = ["Cardiology", "Neurology", "Orthopedics", "Pediatrics", "Dermatology", "Oncology", "NewDepartment"]
```