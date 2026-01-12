import os
import django
import random
import sys

# Setup Django environment
# We check if we are already in a django shell context or need to setup
try:
    from django.conf import settings
    if not settings.configured:
        os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'revana_hms.settings')
        django.setup()
except ImportError:
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'revana_hms.settings')
    try:
        django.setup()
    except Exception as e:
        print(f"Error setting up Django: {e}")
        sys.exit(1)

from accounts.models import User
from hospitals.models import Hospital, Department, Treatment, HospitalAdmin
from doctors.models import Doctor

def create_data():
    print("Starting data population...")
    
    # --- Create Hospitals ---
    cities = ['Vadodara', 'Surat', 'Ahmedabad']
    created_hospitals = []
    
    # List to store admin credentials
    admin_credentials = []

    print("\n--- Hospital Generation ---")
    for city in cities:
        name = f"City Hospital {city}"
        email = f"info_{city.lower()}@cityhospital.com"
        reg_number = f"REG-{city.upper()}-001"
        
        hospital, created = Hospital.objects.get_or_create(
            registration_number=reg_number,
            defaults={
                'name': name,
                'email': email,
                'address': f"Main Road, {city}",
                'phone_number': "9876543210",
                'city': city,
                'state': 'Gujarat',
                'country': 'India',
                'hospital_type': ['general'],
                'status': 'approved',
                'is_approved': True
            }
        )
        created_hospitals.append(hospital)

        # --- Create Hospital Admin ---
        admin_email = f"admin_{city.lower()}@cityhospital.com"
        common_password = "password123"
        
        admin_user, admin_user_created = User.objects.get_or_create(
            email=admin_email,
            defaults={
                'role': 'hospital_admin',
                'is_staff': False,
                'is_active': True,
                'phone': '9876543210'
            }
        )
        
        if admin_user_created:
            admin_user.set_password(common_password)
            admin_user.save()
        else:
            admin_user.set_password(common_password)
            admin_user.save()
            
        HospitalAdmin.objects.get_or_create(
            user=admin_user,
            defaults={'hospital': hospital}
        )
        
        admin_credentials.append({
            'Email': admin_email,
            'Password': common_password,
            'Hospital': hospital.name
        })

        # --- Create Departments & Treatments per Hospital ---
        dept_treatment_map = {
            'Cardiology': ['ECG', 'Angiography', 'Heart Surgery'],
            'Neurology': ['MRI Scan', 'EEG', 'Brain Mapping'],
            'Orthopedics': ['X-Ray', 'Fracture Repair', 'Physiotherapy']
        }
        
        for dept_name, treatment_names in dept_treatment_map.items():
            department, _ = Department.objects.get_or_create(
                hospital=hospital, 
                name=dept_name
            )
            
            for t_name in treatment_names:
                Treatment.objects.get_or_create(
                    hospital=hospital,
                    department=department,
                    name=t_name
                )
    
    print("Hospitals, Admins, and Departments ready.")

    # --- Create Doctors ---
    doctor_credentials = []
    doctor_count = 1
    
    common_password = "password123"

    for hospital in created_hospitals:
        # We want 2 doctors for this hospital
        for _ in range(2):
            email = f"doctor{doctor_count}@test.com"
            
            # Check if user exists first to avoid error if we want to reset password
            user, created = User.objects.get_or_create(
                email=email,
                defaults={
                    'role': 'doctor',
                    'is_staff': False,
                    'is_active': True,
                    'phone': '1234567890'
                }
            )
            
            if created:
                user.set_password(common_password)
                user.save()
            else:
                # Reset password just in case
                user.set_password(common_password)
                user.save()
            
            # Assign to a random department
            departments = list(hospital.departments.all())
            department = random.choice(departments)
            treatments = list(department.treatments.all())
            
            doctor_obj, d_created = Doctor.objects.get_or_create(
                user=user,
                defaults={
                    'name': f"Dr. Test {doctor_count}",
                    'specialization': department.name,
                    'hospital': hospital,
                    'department': department,
                    'status': 'approved',
                    'is_approved': True
                }
            )
            
            # Force update assignment
            doctor_obj.hospital = hospital
            doctor_obj.department = department
            doctor_obj.save()
            doctor_obj.treatments.set(treatments)
            
            doctor_credentials.append({
                'Name': doctor_obj.name,
                'Email': email,
                'Password': common_password,
                'Hospital': hospital.name,
                'Department': department.name
            })
            
            doctor_count += 1
    
    print("\n" + "="*80)
    print("HOSPITAL ADMIN CREDENTIALS")
    print("="*80)
    print(f"{'Email':<35} | {'Password':<15} | {'Hospital':<25}")
    print("-" * 80)
    for admin in admin_credentials:
        print(f"{admin['Email']:<35} | {admin['Password']:<15} | {admin['Hospital']:<25}")
    print("-" * 80)

    print("\n" + "="*110)
    print("DOCTOR CREDENTIALS")
    print("="*110)
    print(f"{'Name':<20} | {'Email':<25} | {'Password':<15} | {'Hospital':<25} | {'Department':<15}")
    print("-" * 110)
    for doc in doctor_credentials:
        print(f"{doc['Name']:<20} | {doc['Email']:<25} | {doc['Password']:<15} | {doc['Hospital']:<25} | {doc['Department']:<15}")
    print("-" * 110)

if __name__ == "__main__":
    create_data()
