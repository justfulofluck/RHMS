import os
import django
import sys

# Setup Django environment
sys.path.append('/home/bhavan/Desktop/RHMS/revana_hms')
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'revana_hms.settings')
django.setup()

from hospitals.models import Hospital, HospitalAdmin
from django.core.mail import send_mail
from django.conf import settings

def debug_approve(hospital_id):
    print(f"Attempting to approve hospital {hospital_id}")
    try:
        hospital = Hospital.objects.get(id=hospital_id)
        print(f"Found hospital: {hospital.name}")
        
        hospital.status = Hospital.STATUS_APPROVED
        hospital.is_approved = True
        hospital.save()
        print("Hospital saved as approved")

        try:
            admin = HospitalAdmin.objects.get(hospital=hospital)
            print(f"Found admin: {admin}")
            admin.user.is_active = True
            admin.user.save()
            print("Admin user activated")
            
            print("Sending email...")
            send_mail(
                subject='Hospital Registration Approved',
                message='Your hospital registration has been approved. You can now login to your dashboard.',
                from_email='blueglobalcloud@gmail.com',
                recipient_list=[hospital.email],
                fail_silently=False,
            )
            print("Email sent")
            
        except HospitalAdmin.DoesNotExist:
            print("HospitalAdmin.DoesNotExist caught")
        except Exception as e:
            print(f"Error in inner block: {e}")
            import traceback
            traceback.print_exc()

    except Exception as e:
        print(f"Error in outer block: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    debug_approve(62)
