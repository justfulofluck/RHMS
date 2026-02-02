
import os
import django
import random
from faker import Faker

# Setup Django Environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'revana_hms.settings')
django.setup()

from django.contrib.auth import get_user_model
from hospitals.models import Hospital
from patients.models import Patient

fake = Faker('en_IN')
User = get_user_model()

# List of OLD Patient emails to cleanup (from population.md)
OLD_PATIENT_EMAILS = [
    "zvig@example.net", "rachanarai@example.org", "darsh96@example.net", 
    "etasingh@example.com", "venkataramanwridesh@example.com", "khuranadiya@example.com", 
    "revamodi@example.net", "anmolgokhale@example.net", "atank@example.net", 
    "lucky58@example.net", "elijahrajan@example.net", "meerarastogi@example.com", 
    "aahana89@example.com", "radha53@example.com", "aadhyakari@example.org", 
    "jhalak01@example.org", "fariqsubramaniam@example.com", "baljiwan22@example.net", 
    "hemanginishetty@example.net", "kaulanay@example.org", "qpurohit@example.org", 
    "kauraditya@example.net", "sibalisaac@example.net", "aaravgour@example.org", 
    "parth92@example.org", "chasmum52@example.net", "hemabath@example.com", 
    "omyahanda@example.net", "yashicamore@example.org", "krish52@example.com", 
    "sulechandani@example.net", "magarfariq@example.com", "dhriti43@example.com", 
    "tray@example.net", "sodhiumang@example.net", "hhans@example.org", 
    "imarandeo@example.net", "ethanpatil@example.net", "dugarjanaki@example.net", 
    "yogikabir@example.org", "amrutarattan@example.org", "qsalvi@example.net", 
    "pranav51@example.com", "zansi55@example.net", "pranit05@example.org", 
    "jsami@example.com", "dwadhwa@example.org", "masonyadav@example.net", 
    "esarna@example.com", "bvarma@example.org", "msharma@example.org", 
    "ekanidey@example.net", "nidhi67@example.com", "mnadig@example.com", 
    "nbera@example.org", "shroffanya@example.org", "qparmar@example.com", 
    "tdas@example.com", "nidra23@example.com", "sacharjanaki@example.net"
]

def cleanup_old_patients():
    print(f"Checking for {len(OLD_PATIENT_EMAILS)} old patients to cleanup...")
    count = 0
    for email in OLD_PATIENT_EMAILS:
        try:
            user = User.objects.get(email=email)
            user.delete() # Cascades to Patient profile
            count += 1
        except User.DoesNotExist:
            pass
    print(f"Cleanup complete. Deleted {count} patients.")

def create_new_patients(count=60):
    print(f"Creating {count} new active Patients...")
    
    hospitals = list(Hospital.objects.filter(status='approved'))
    
    created_count = 0
    gender_choices = ["Male", "Female", "Other"]

    for _ in range(count):
        fake_name = fake.first_name() + " " + fake.last_name()
        clean_name = "".join(e for e in fake_name if e.isalnum()).lower()
        email = f"patient_{clean_name}_{random.randint(1000,9999)}@rhms.com"
        
        try:
            # 1. Create User
            user, created = User.objects.get_or_create(email=email)
            if not created:
                continue
                
            user.set_password("patient123")
            user.role = 'patient'
            user.is_active = True
            user.save()

            # 2. Create Patient Profile
            Patient.objects.create(
                user=user,
                name=fake_name,
                age=random.randint(18, 85),
                gender=random.choice(gender_choices),
                phone=fake.phone_number(),
                address=fake.address(),
                hospital=random.choice(hospitals) if hospitals else None,
                medical_history=fake.sentence(),
                # photo can be blank
            )
            
            created_count += 1
            if created_count % 10 == 0:
                print(f"Created {created_count} patients...")
            
        except Exception as e:
            print(f"Error creating patient {email}: {e}")

    print(f"Successfully created {created_count} new patients.")

if __name__ == "__main__":
    cleanup_old_patients()
    create_new_patients(60)
