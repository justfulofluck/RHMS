import os
import django
import json
import sys

# Setup Django Environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'revana_hms.settings')
django.setup()

from django.contrib.auth import get_user_model
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.test import APIClient
from doctors.models import Doctor, Department, Hospital, Treatment

User = get_user_model()

def run_verification():
    # 1. Create/Get a Test User (Patient Role to see public doctors)
    email = "api_tester@example.com"
    password = "testpassword123"
    
    try:
        user = User.objects.get(email=email)
        print(f"Found existing user: {email}")
    except User.DoesNotExist:
        user = User.objects.create_user(email=email, password=password, role='patient')
        print(f"Created new test user: {email}")

    # 2. Generate Token
    refresh = RefreshToken.for_user(user)
    access_token = str(refresh.access_token)
    
    print("\n" + "="*50)
    print("GENERATED VALID TOKEN")
    print("="*50)
    print(f"Bearer {access_token}")
    print("="*50 + "\n")

    # 3. Ensure we have some data to see
    # If no approved doctors exist, the list might be empty.
    # Let's try to query first.
    
    client = APIClient()
    client.credentials(HTTP_AUTHORIZATION=f'Bearer {access_token}')
    
    print("Executing: GET /api/doctors/")
    response = client.get('/api/doctors/')
    
    if response.status_code == 200:
        print("\nSUCCESS: API returned 200 OK")
        print("Response Data (First 2 items):")
        data = response.json()
        print(json.dumps(data[:2], indent=4) if isinstance(data, list) else json.dumps(data, indent=4))
        
        if not data:
            print("\nNOTE: The list is empty. This means there are no 'Approved' doctors in the database.")
            print("You might need to log in as a Superuser or Hospital Admin to see pending doctors,")
            print("or approve a doctor in the database first.")
    else:
        print(f"\nFAILED: Status Code {response.status_code}")
        print(response.json())

if __name__ == "__main__":
    run_verification()
