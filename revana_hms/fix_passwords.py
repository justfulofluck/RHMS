
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'revana_hms.settings')
django.setup()

from django.contrib.auth import get_user_model
from accounts.models import User

def fix_passwords():
    print("Fixing passwords for all users...")
    
    # 1. Doctors
    doctor_users = User.objects.filter(role='doctor')
    for user in doctor_users:
        user.set_password('doctor123')
        user.save()
    print(f"Updated {doctor_users.count()} doctors.")

    # 2. Hospital Admins
    admin_users = User.objects.filter(role='hospital_admin')
    for user in admin_users:
        user.set_password('admin123')
        user.save()
    print(f"Updated {admin_users.count()} admins.")

    # 3. Patients
    patient_users = User.objects.filter(role='patient')
    for user in patient_users:
        user.set_password('patient123')
        user.save()
    print(f"Updated {patient_users.count()} patients.")

if __name__ == "__main__":
    fix_passwords()
    print("Done! 🚀")
