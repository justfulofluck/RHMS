import os
import shutil
from django.core.management.base import BaseCommand
from django.conf import settings
from hospitals.models import Hospital
from patients.models import Patient

class Command(BaseCommand):
    help = 'Migrates media files to the new directory structure'

    def handle(self, *args, **kwargs):
        self.stdout.write("Starting media migration...")

        # --- MIGRATE HOSPITALS ---
        self.stdout.write("Migrating Hospitals...")
        hospitals = Hospital.objects.all()
        for hospital in hospitals:
            if hospital.logo:
                old_path = os.path.join(settings.MEDIA_ROOT, str(hospital.logo))
                if os.path.exists(old_path) and 'hospital_logos/' in str(hospital.logo):
                    # Define new path
                    ext = os.path.splitext(old_path)[1]
                    new_filename = f"logo{ext}"
                    new_rel_dir = f"hospitals/{hospital.id}"
                    new_dir = os.path.join(settings.MEDIA_ROOT, new_rel_dir)
                    new_path = os.path.join(new_dir, new_filename)

                    # Create directory
                    os.makedirs(new_dir, exist_ok=True)

                    # Move file
                    try:
                        shutil.move(old_path, new_path)
                        # Update DB
                        hospital.logo = f"{new_rel_dir}/{new_filename}"
                        hospital.save()
                        self.stdout.write(self.style.SUCCESS(f"Moved logo for Hospital {hospital.id}"))
                    except Exception as e:
                        self.stdout.write(self.style.ERROR(f"Failed to move logo for Hospital {hospital.id}: {e}"))
                elif not os.path.exists(old_path):
                     self.stdout.write(self.style.WARNING(f"Logo file not found for Hospital {hospital.id}: {old_path}"))

        # --- MIGRATE PATIENTS ---
        self.stdout.write("\nMigrating Patients...")
        patients = Patient.objects.all()
        for patient in patients:
            if patient.photo:
                old_path = os.path.join(settings.MEDIA_ROOT, str(patient.photo))
                if os.path.exists(old_path) and 'patients/photos/' in str(patient.photo):
                    # Define new path
                    ext = os.path.splitext(old_path)[1]
                    new_filename = f"profile{ext}"
                    new_rel_dir = f"patients/{patient.id}"
                    new_dir = os.path.join(settings.MEDIA_ROOT, new_rel_dir)
                    new_path = os.path.join(new_dir, new_filename)

                    # Create directory
                    os.makedirs(new_dir, exist_ok=True)

                    # Move file
                    try:
                        shutil.move(old_path, new_path)
                        # Update DB
                        patient.photo = f"{new_rel_dir}/{new_filename}"
                        patient.save()
                        self.stdout.write(self.style.SUCCESS(f"Moved photo for Patient {patient.id}"))
                    except Exception as e:
                        self.stdout.write(self.style.ERROR(f"Failed to move photo for Patient {patient.id}: {e}"))
                elif not os.path.exists(old_path):
                     self.stdout.write(self.style.WARNING(f"Photo file not found for Patient {patient.id}: {old_path}"))

        self.stdout.write(self.style.SUCCESS("\nMedia migration completed!"))
