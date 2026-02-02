import os
import django
from django.utils import timezone
from datetime import timedelta

# Setup Django Environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'revana_hms.settings')
django.setup()

from django.contrib.auth import get_user_model
User = get_user_model()

def get_details(user):
    try:
        if user.role == 'doctor':
            doc = user.doctor
            return doc.name, f"{doc.hospital.name} ({doc.department.name})"
        elif user.role == 'patient':
            pat = user.patient
            params = f"Assigned: {pat.hospital.name}" if pat.hospital else "Unassigned"
            return pat.name, params
        elif user.role == 'hospital_admin':
            if hasattr(user, 'hospitaladminprofile'):
                admin_name = user.hospitaladminprofile.name
                # Try to get hospital from HospitalAdmin relation
                try:
                    h_admin = user.hospitaladmin
                    h_name = h_admin.hospital.name if h_admin else "No Hospital"
                except Exception as e:
                    h_name = f"Error: {e}"
                return admin_name, h_name
            return "Admin", "Unknown"
    except Exception as e:
        return "Unknown", str(e)
    return "User", "-"

def generate_markdown():
    # Filter users created in the last 24 hours (Test Data)
    start_time = timezone.now() - timedelta(hours=24)
    users = User.objects.filter(date_joined__gte=start_time).exclude(is_superuser=True).order_by('role', 'date_joined')
    
    file_path = "population.md"
    
    with open(file_path, "w") as f:
        f.write("# 🧪 Test Data Credentials\n\n")
        f.write("> **Note:** All test accounts use the password: `password123`\n\n")
        
        # Group by role
        roles = {}
        for user in users:
            role = user.role.replace("_", " ").title()
            if role not in roles:
                roles[role] = []
            roles[role].append(user)
            
        for role, user_list in roles.items():
            f.write(f"## 👤 {role}s ({len(user_list)})\n")
            f.write("| Name | Assignment | Email (Username) | Password |\n")
            f.write("|------|------------|------------------|----------|\n")
            
            for user in user_list:
                name, assignment = get_details(user)
                f.write(f"| {name} | {assignment} | `{user.email}` | `password123` |\n")
            f.write("\n")
            
    print(f"✅ Successfully created {file_path} with {users.count()} users.")

if __name__ == "__main__":
    generate_markdown()
