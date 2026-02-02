import random
from faker import Faker
from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from django.utils import timezone
from hospitals.models import Hospital, Department, Treatment, HospitalAdmin
from doctors.models import Doctor, DoctorProfile
from patients.models import Patient
import os

User = get_user_model()
fake = Faker('en_IN')
PASSWORD = "password123"

LOCATIONS = ["Surat", "Ahmedabad", "Vadodara", "Gandhinagar", "Rajkot"]

DEPARTMENTS = {
    "Cardiology": ["ECG", "Angiography", "Angioplasty"],
    "Orthopedics": ["Fracture Treatment", "Joint Replacement", "Physiotherapy"],
    "Neurology": ["MRI Scan", "EEG", "Stroke Management"],
    "Pediatrics": ["Vaccination", "General Checkup", "Growth Monitoring"],
    "General Medicine": ["Fever Treatment", "Diabetes Management", "Blood Pressure Check"]
}

class Command(BaseCommand):
    help = 'Populate the database with test data'

    def handle(self, *args, **kwargs):
        self.stdout.write("Starting data population...")
        
        # 1. Create Hospitals (5)
        self.stdout.write("Creating Hospitals...")
        hospitals = []
        for city in LOCATIONS:
            hospital_name = f"City Hospital {city}"
            hospital, created = Hospital.objects.get_or_create(
                name=hospital_name,
                defaults={
                    'email': f"info_{city.lower()}@cityhospital.com",
                    'registration_number': f"REG-{city[:3].upper()}-{random.randint(1000, 9999)}",
                    'address': fake.address(),
                    'phone_number': fake.phone_number(),
                    'city': city,
                    'status': Hospital.STATUS_APPROVED,
                    'is_approved': True,
                    'hospital_type': ["general", "multispeciality"],
                    'hours': {"Mon-Fri": "9am-9pm"}
                }
            )
            if created:
                self.stdout.write(f"  Created: {hospital.name}")
            hospitals.append(hospital)

            # Create Departments & Treatments for this hospital
            for dept_name, treatments in DEPARTMENTS.items():
                dept, _ = Department.objects.get_or_create(hospital=hospital, name=dept_name)
                for treatment_name in treatments:
                    Treatment.objects.get_or_create(hospital=hospital, department=dept, name=treatment_name)

        # 2. Create Hospital Admins (20 - 4 per hospital)
        self.stdout.write("Creating Hospital Admins...")
        for hospital in hospitals:
            for i in range(4):
                email = f"admin_{hospital.city.lower()}_{i+1}@rhms.com"
                if not User.objects.filter(email=email).exists():
                    user = User.objects.create_user(
                        email=email,
                        password=PASSWORD,
                        role='hospital_admin',
                        is_staff=True
                    )
                    HospitalAdmin.objects.create(user=user, hospital=hospital)
                    self.stdout.write(f"  Created Admin: {email}")

        # 3. Create Doctors (50 - 10 per hospital)
        self.stdout.write("Creating Doctors...")
        for hospital in hospitals:
            departments = list(hospital.departments.all())
            for i in range(10):
                first_name = fake.first_name()
                last_name = fake.last_name()
                email = f"dr.{first_name.lower()}.{last_name.lower()}@rhms.com"
                
                if User.objects.filter(email=email).exists():
                    continue

                user = User.objects.create_user(
                    email=email,
                    password=PASSWORD,
                    role='doctor'
                )
                
                dept = random.choice(departments)
                
                # Create Doctor Profile
                DoctorProfile.objects.create(
                    user=user,
                    gender=random.choice(['Male', 'Female']),
                    date_of_birth=fake.date_of_birth(minimum_age=30, maximum_age=60),
                    contact_number=fake.phone_number(),
                    address=fake.address(),
                    qualification=random.choice(["MBBS", "MD", "MS", "BAMS"]),
                    specialization=dept.name,
                    year_of_experience=random.randint(2, 25),
                    aadhaar=f"{random.randint(1000,9999)} {random.randint(1000,9999)} {random.randint(1000,9999)}"
                )

                # Create Doctor Entry
                doctor = Doctor.objects.create(
                    user=user,
                    name=f"Dr. {first_name} {last_name}",
                    hospital=hospital,
                    department=dept,
                    specialization=dept.name,
                    status=Doctor.STATUS_APPROVED,
                    is_approved=True
                )
                
                # Assign some treatments
                treatments = list(dept.treatments.all())
                if treatments:
                    doctor.treatments.add(*random.sample(treatments, k=min(len(treatments), 3)))

                self.stdout.write(f"  Created Doctor: {doctor.name} ({hospital.city})")

        # 4. Create Patients (60 - Distributed)
        self.stdout.write("Creating Patients...")
        for i in range(60):
            first_name = fake.first_name()
            email = f"patient_{i+1}_{first_name.lower()}@gmail.com"
            
            if User.objects.filter(email=email).exists():
                continue

            user = User.objects.create_user(
                email=email,
                password=PASSWORD,
                role='patient'
            )

            hospital = random.choice(hospitals)
            
            Patient.objects.create(
                user=user,
                name=f"{first_name} {fake.last_name()}",
                hospital=hospital,
                age=random.randint(18, 90),
                gender=random.choice(['Male', 'Female']),
                phone=fake.phone_number(),
                address=fake.address()
            )
            self.stdout.write(f"  Created Patient: {email}")

        self.stdout.write(self.style.SUCCESS('Successfully populated database!'))
