#!/usr/bin/env python3
"""
Test script for the doctors API endpoint with hospital_id filter
"""
import os
import django
import requests
import json

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'revana_hms.settings')
django.setup()

from doctors.models import Doctor, DoctorAvailability
from hospitals.models import Hospital

def test_api():
    base_url = "http://localhost:8000/api/doctors/"
    
    print("🏥 Testing Doctors API Endpoint")
    print("=" * 50)
    
    # Test 1: Get all hospitals
    print("\n📋 Available Hospitals:")
    hospitals = Hospital.objects.all()
    for h in hospitals[:5]:  # Show first 5
        print(f"  ID: {h.id}, Name: {h.name}, Status: {h.status}")
    
    # Test 2: Get all doctors
    print("\n👨‍⚕️ All Doctors in DB:")
    doctors = Doctor.objects.select_related('hospital').all()
    for d in doctors:
        print(f"  ID: {d.id}, Name: {d.name}, Hospital: {d.hospital.name} (ID: {d.hospital.id}), Status: {d.status}")
    
    # Test 3: API without hospital_id
    print("\n🔍 API Test 1: /api/doctors/")
    try:
        response = requests.get(base_url)
        print(f"  Status: {response.status_code}")
        print(f"  Response: {response.json()}")
    except Exception as e:
        print(f"  Error: {e}")
    
    # Test 4: API with hospital_id (Test Hospital - ID 26)
    print("\n🔍 API Test 2: /api/doctors/?hospital_id=26")
    try:
        response = requests.get(f"{base_url}?hospital_id=26")
        print(f"  Status: {response.status_code}")
        print(f"  Response: {response.json()}")
    except Exception as e:
        print(f"  Error: {e}")
    
    # Test 5: API with hospital_id (Ramanathan Hospital - ID 1)  
    print("\n🔍 API Test 3: /api/doctors/?hospital_id=1")
    try:
        response = requests.get(f"{base_url}?hospital_id=1")
        print(f"  Status: {response.status_code}")
        print(f"  Response: {response.json()}")
    except Exception as e:
        print(f"  Error: {e}")
    
    # Test 6: Check what the DoctorViewSet.get_queryset() returns for different user types
    print("\n🧪 Testing QuerySet Logic:")
    
    # Simulate unauthenticated user (patient view)
    from doctors.views import DoctorViewSet
    from django.http import HttpRequest
    from django.contrib.auth.models import AnonymousUser
    
    class MockRequest:
        def __init__(self, user=None):
            self.user = user or AnonymousUser()
    
    # Test with anonymous user
    viewset = DoctorViewSet()
    viewset.request = MockRequest()
    queryset = viewset.get_queryset()
    print(f"  Anonymous user queryset count: {queryset.count()}")
    
    # Test with hospital_id filter
    print(f"  Anonymous user with hospital_id=26: {queryset.filter(hospital_id=26).count()}")
    
    print("\n✅ Testing Complete!")

if __name__ == "__main__":
    test_api()