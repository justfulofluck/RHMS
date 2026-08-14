import io
from datetime import date, timedelta

from django.core.files.base import ContentFile
from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from PIL import Image

from accounts.models import DoctorProfile
from hospitals.models import Hospital, HospitalAdmin, Department, Treatment
from doctors.models import Doctor

User = get_user_model()

ADMIN_PASSWORD = "Admin@123"
DOCTOR_PASSWORD = "Doctor@123"

DEPARTMENTS = {
    "Cardiology": ["ECG", "Angiography", "Angioplasty"],
    "Orthopedics": ["Fracture Treatment", "Joint Replacement", "Physiotherapy"],
    "General Medicine": ["Fever Treatment", "Diabetes Management", "Blood Pressure Check"],
}

HOSPITALS = [
    {
        "name": "Blue Global Hospital",
        "registration_number": "REG-BGH-1001",
        "email": "info@blueglobalhospital.com",
        "address": "101, Ring Road, Adajan, Surat",
        "phone_number": "+91 98765 43210",
        "city": "Surat",
        "admin_email": "admin1@blueglobalhospital.com",
        "doctors": [
            {
                "name": "Dr. Aarav Mehta",
                "email": "dr.aarav.mehta@blueglobalhospital.com",
                "specialization": "Cardiologist",
                "department": "Cardiology",
                "gender": "Male",
                "date_of_birth": date(1985, 3, 14),
                "contact_number": "+91 98111 22334",
                "address": "22, Diamond Residency, Vesu, Surat",
                "qualification": "MD, DM (Cardiology)",
                "year_of_experience": 14,
                "aadhaar": "4523 7812 9034",
            },
            {
                "name": "Dr. Priya Sharma",
                "email": "dr.priya.sharma@blueglobalhospital.com",
                "specialization": "Orthopedic Surgeon",
                "department": "Orthopedics",
                "gender": "Female",
                "date_of_birth": date(1988, 9, 2),
                "contact_number": "+91 98222 33445",
                "address": "7, Shubham Society, Pal, Surat",
                "qualification": "MS (Orthopedics)",
                "year_of_experience": 10,
                "aadhaar": "7812 9034 4523",
            },
        ],
    },
    {
        "name": "Revana Care Multispeciality Hospital",
        "registration_number": "REG-RCM-2002",
        "email": "info@revanacare.com",
        "address": "55, SG Highway, Satellite, Ahmedabad",
        "phone_number": "+91 91234 56780",
        "city": "Ahmedabad",
        "admin_email": "admin2@revanacare.com",
        "doctors": [
            {
                "name": "Dr. Rohan Patel",
                "email": "dr.rohan.patel@revanacare.com",
                "specialization": "Cardiologist",
                "department": "Cardiology",
                "gender": "Male",
                "date_of_birth": date(1980, 12, 25),
                "contact_number": "+91 90909 11223",
                "address": "12, Green Villa, Navrangpura, Ahmedabad",
                "qualification": "MD, DM (Cardiology)",
                "year_of_experience": 18,
                "aadhaar": "3345 5678 1122",
            },
            {
                "name": "Dr. Sneha Iyer",
                "email": "dr.sneha.iyer@revanacare.com",
                "specialization": "General Physician",
                "department": "General Medicine",
                "gender": "Female",
                "date_of_birth": date(1990, 6, 18),
                "contact_number": "+91 98765 55443",
                "address": "3, Sunrise Apartments, Bodakdev, Ahmedabad",
                "qualification": "MBBS, MD (General Medicine)",
                "year_of_experience": 8,
                "aadhaar": "9988 7766 5544",
            },
        ],
    },
]


def make_png_bytes(size=(64, 64), color=(52, 152, 219)):
    """Return bytes of a tiny valid PNG image."""
    img = Image.new("RGB", size, color)
    buf = io.BytesIO()
    img.save(buf, format="PNG")
    return buf.getvalue()


def make_file_bytes():
    return b"Placeholder certificate for demo data."


class Command(BaseCommand):
    help = "Seed demo data: 2 approved hospitals, 2 hospital admins, 4 doctors (2 per hospital)."

    def handle(self, *args, **options):
        self.stdout.write(self.style.WARNING("Seeding demo data..."))

        for hospital_data in HOSPITALS:
            hospital, created = Hospital.objects.get_or_create(
                email=hospital_data["email"],
                defaults={
                    "name": hospital_data["name"],
                    "registration_number": hospital_data["registration_number"],
                    "address": hospital_data["address"],
                    "phone_number": hospital_data["phone_number"],
                    "city": hospital_data["city"],
                    "state": "Gujarat",
                    "country": "India",
                    "status": Hospital.STATUS_APPROVED,
                    "is_approved": True,
                    "hospital_type": ["general", "multispeciality"],
                    "hours": {"Mon-Sat": "9am-9pm", "Sun": "10am-2pm"},
                },
            )
            self.stdout.write(self.style.SUCCESS(f"  {'Created' if created else 'Found'} Hospital: {hospital.name} ({hospital.city})"))

            for dept_name, treatments in DEPARTMENTS.items():
                dept, _ = Department.objects.get_or_create(hospital=hospital, name=dept_name)
                for treatment_name in treatments:
                    Treatment.objects.get_or_create(hospital=hospital, department=dept, name=treatment_name)

            admin_user, admin_created = User.objects.get_or_create(
                email=hospital_data["admin_email"],
                defaults={"role": "hospital_admin", "is_staff": True, "is_active": True, "phone": hospital_data["phone_number"]},
            )
            admin_user.role = "hospital_admin"
            admin_user.is_staff = True
            admin_user.is_active = True
            admin_user.set_password(ADMIN_PASSWORD)
            admin_user.save()
            HospitalAdmin.objects.update_or_create(hospital=hospital, defaults={"user": admin_user})
            self.stdout.write(self.style.SUCCESS(f"  {'Created' if admin_created else 'Updated'} Admin: {admin_user.email}"))

            for doc_data in hospital_data["doctors"]:
                user, user_created = User.objects.get_or_create(
                    email=doc_data["email"],
                    defaults={"role": "doctor", "is_active": True, "phone": doc_data["contact_number"]},
                )
                user.role = "doctor"
                user.is_active = True
                user.phone = doc_data["contact_number"]
                user.set_password(DOCTOR_PASSWORD)
                user.save()

                DoctorProfile.objects.update_or_create(
                    user=user,
                    defaults={
                        "gender": doc_data["gender"],
                        "date_of_birth": doc_data["date_of_birth"],
                        "contact_number": doc_data["contact_number"],
                        "address": doc_data["address"],
                        "qualification": doc_data["qualification"],
                        "specialization": doc_data["specialization"],
                        "year_of_experience": doc_data["year_of_experience"],
                        "aadhaar": doc_data["aadhaar"],
                        "medical_certificate": ContentFile(make_file_bytes(), name="medical_certificate.pdf"),
                        "registration_certificate": ContentFile(make_file_bytes(), name="registration_certificate.pdf"),
                        "degree_certificates": ContentFile(make_file_bytes(), name="degree_certificates.pdf"),
                        "passport_photo": ContentFile(make_png_bytes(), name="passport_photo.png"),
                        "experience_certificate": ContentFile(make_file_bytes(), name="experience_certificate.pdf"),
                    },
                )

                dept = Department.objects.get(hospital=hospital, name=doc_data["department"])
                doctor, doctor_created = Doctor.objects.update_or_create(
                    user=user,
                    defaults={
                        "name": doc_data["name"],
                        "hospital": hospital,
                        "department": dept,
                        "specialization": doc_data["specialization"],
                        "status": Doctor.STATUS_APPROVED,
                        "is_approved": True,
                    },
                )
                doctor.treatments.set(list(dept.treatments.all()))
                self.stdout.write(self.style.SUCCESS(f"  {'Created' if user_created else 'Updated'} Doctor: {doctor.name} -> {hospital.name}"))

        self.stdout.write(self.style.SUCCESS("Done. Credentials:"))
        for hospital_data in HOSPITALS:
            self.stdout.write(self.style.WARNING(f"  Admin: {hospital_data['admin_email']} / {ADMIN_PASSWORD}"))
            for doc_data in hospital_data["doctors"]:
                self.stdout.write(self.style.WARNING(f"  Doctor: {doc_data['email']} / {DOCTOR_PASSWORD}"))