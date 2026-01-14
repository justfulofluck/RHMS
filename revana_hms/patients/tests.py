from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth import get_user_model
from rest_framework.test import APITestCase
from rest_framework import status
from .models import Patient

User = get_user_model()

class PatientProfileApiTest(APITestCase):
    def setUp(self):
        # Create a test user
        self.email = 'apitest@example.com'
        self.password = 'testpass123'
        self.user = User.objects.create_user(email=self.email, password=self.password)
        self.user.role = 'patient'
        self.user.save()
        
        # Create a linked patient profile
        self.patient = Patient.objects.create(
            user=self.user, 
            name="Old API Name", 
            age=30, 
            gender="Male", 
            phone="1234567890", 
            address="123 API St"
        )
        
        # Authenticate for API testing
        self.client.force_authenticate(user=self.user)

    def test_get_profile_returns_correct_name(self):
        """Test that the API returns the name from the Patient model."""
        url = reverse('api_patient_profile')
        response = self.client.get(url)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['name'], "Old API Name")
        self.assertEqual(response.data['email'], self.email)

    def test_update_profile_name_via_api(self):
        """Test updating the name field via the API."""
        url = reverse('api_patient_profile')
        data = {'name': 'New API Name'}
        
        # Perform PATCH request
        response = self.client.patch(url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['name'], 'New API Name')
        
        # Verify database update
        self.patient.refresh_from_db()
        self.assertEqual(self.patient.name, 'New API Name')

class PatientProfileWebTest(TestCase):
    def setUp(self):
        # Create a test user
        self.email = 'webtest@example.com'
        self.password = 'testpass123'
        self.user = User.objects.create_user(email=self.email, password=self.password)
        self.user.role = 'patient'
        self.user.save()
        
        # Create a linked patient profile
        self.patient = Patient.objects.create(
            user=self.user, 
            name="Old Web Name", 
            age=25, 
            gender="Female", 
            phone="0987654321", 
            address="456 Web Ave"
        )
        
        # Log in for Web testing
        self.client.force_login(self.user)

    def test_update_profile_name_via_web_form(self):
        """Test updating the name field via the Web Edit Profile form."""
        url = reverse('patient_edit_profile')
        data = {
            'name': 'New Web Name',
            # Add other fields if required by form validation, but usually name is enough for update
        }
        
        # Perform POST request
        response = self.client.post(url, data, follow=True)
        
        self.assertEqual(response.status_code, 200)
        
        # Verify database update
        self.patient.refresh_from_db()
        self.assertEqual(self.patient.name, 'New Web Name')
