from django import forms
from .models import Hospital

class HospitalRegistrationForm(forms.ModelForm):
    class Meta:
        model = Hospital
        fields = ['name', 'registration_number', 'email', 'logo', 'address', 'phone_number', 'city']
