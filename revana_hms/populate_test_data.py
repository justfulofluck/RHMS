import os
import django
import random
from faker import Faker
from datetime import timedelta, date

# Setup Django Environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'revana_hms.settings')
django.setup()

from django.contrib.auth import get_user_model
from hospitals.models import Hospital, HospitalAdmin, Department, Treatment
from doctors.models import Doctor
from patients.models import Patient
# Note: DoctorProfile and HospitalAdminProfile require file uploads, so we'll skip them for demo data

User = get_user_model()  # Use the custom User model
fake = Faker('en_IN')

# Constants
CITIES = ["Surat", "Ahmedabad", "Vadodara", "Gandhinagar", "Rajkot"]
DEPARTMENTS = ["Cardiology", "Neurology", "Orthopedics", "Pediatrics", "Dermatology", "Oncology"]
TITLES = ["Dr. ", "Dr. (Mrs.) ", "Dr. (Ms.) "]

def create_hospitals():
    print("Creating Hospitals...")
    hospitals = []
    for city in CITIES:
        for _ in range(2): # 2 hospitals per city to distribute standard load
            name = f"{fake.last_name()} Hospital {city}"
            hospital = Hospital.objects.create(
                name=name,
                registration_number=fake.uuid4(),
                email=fake.email(),
                address=fake.address(),
                phone_number=fake.phone_number(),
                city=city,
                state="Gujarat",
                country="India",
                status=Hospital.STATUS_APPROVED,
                is_approved=True,
                hospital_type=["general"],
                hours={"open": "09:00", "close": "20:00"}
            )
            
            # Create Departments & Treatments
            for dept_name in random.sample(DEPARTMENTS, 3):
                dept = Department.objects.create(hospital=hospital, name=dept_name)
                Treatment.objects.create(hospital=hospital, department=dept, name=f"{dept_name} Consultation")
                Treatment.objects.create(hospital=hospital, department=dept, name=f"{dept_name} Surgery")
            
            hospitals.append(hospital)
    print(f"Created {len(hospitals)} hospitals.")
    return hospitals

def create_admins(hospitals, count=20):
    print(f"Creating {count} Hospital Admins...")
    for _ in range(count):
        hospital = random.choice(hospitals)
        email = fake.unique.email()
        
        user = User.objects.create_user(
            email=email,
            password="admin123",
            role="hospital_admin",
            is_active=True,
            is_staff=True
        )
        
        HospitalAdmin.objects.create(user=user, hospital=hospital)
        
        # Note: Skipping HospitalAdminProfile creation due to potential required fields
        # In a real application, you would create the profile with proper data
    print("Admins created.")

def create_doctors(hospitals, count=50):
    print(f"Creating {count} Doctors...")
    doctors_per_hospital = count // len(hospitals)
    remainder = count % len(hospitals)  # Distribute remaining doctors to first hospitals
    
    for i, hospital in enumerate(hospitals):
        # Distribute remainder to first few hospitals
        doctors_for_this_hospital = doctors_per_hospital + (1 if i < remainder else 0)
        
        for _ in range(doctors_for_this_hospital):
            departments = hospital.departments.all()
            if not departments.exists():
                print(f"Skipping hospital {hospital.name} - no departments")
                continue
            department = random.choice(departments)
            
            first_name = fake.first_name()
            last_name = fake.last_name()
            name = f"{random.choice(TITLES)}{first_name} {last_name}"
            email = fake.unique.email()
            
            # Create User
            user = User.objects.create_user(
                email=email,
                password="doctor123",
                role="doctor",
                is_active=True
            )
            
            # Note: Skipping DoctorProfile creation due to required file fields
            # For demo data, we'll create only the Doctor record
            
            # Create Doctor Record
            doc = Doctor.objects.create(
                user=user,
                name=name,
                specialization=department.name,
                hospital=hospital,
                department=department,
                status=Doctor.STATUS_APPROVED,
                is_approved=True
            )
            # Assign treatments
            treatments = department.treatments.all()
            if treatments.exists():
                doc.treatments.set(treatments)
                
    print("Doctors created.")

def create_patients(hospitals, count=60):
    print(f"Creating {count} Patients...")
    patients_per_hospital = count // len(hospitals)
    remainder = count % len(hospitals)  # Distribute remaining patients to first hospitals
    
    for i, hospital in enumerate(hospitals):
        # Distribute remainder to first few hospitals
        patients_for_this_hospital = patients_per_hospital + (1 if i < remainder else 0)
        
        for _ in range(patients_for_this_hospital):
            first_name = fake.first_name()
            last_name = fake.last_name()
            email = fake.unique.email()
            
            user = User.objects.create_user(
                email=email,
                password="patient123",
                role="patient",
                is_active=True
            )
            
            # Use hospital's city for address
            city = hospital.city
            
            Patient.objects.create(
                user=user,
                name=f"{first_name} {last_name}",
                hospital=hospital,  # Guaranteed assignment
                age=random.randint(18, 90),
                gender=random.choice(["Male", "Female", "Other"]),
                phone=fake.phone_number(),
                address=f"{fake.street_address()}, {city}, Gujarat",
                medical_history=fake.text()
            )
    print("Patients created.")

if __name__ == "__main__":
    print("Starting data population...")
    hospitals = create_hospitals()
    create_admins(hospitals, 20)
    create_doctors(hospitals, 50)
    create_patients(hospitals, 60)
    print("Data population complete! 🚀")