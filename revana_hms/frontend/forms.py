from django import forms
from django.contrib.auth.models import User
from hospitals.models import Hospital

class HospitalRegistrationForm(forms.Form):
    name = forms.CharField(label='Hospital Name', max_length=100)
    registration_number = forms.CharField(label='Registration Number', max_length=50)
    email = forms.EmailField(label='Email')
    contact_number = forms.CharField(label='Contact Number', max_length=15)
    address = forms.CharField(widget=forms.Textarea)
    city = forms.CharField(max_length=50)
    state = forms.CharField(max_length=50)
    country = forms.CharField(max_length=50)
    hospital_type = forms.CharField(max_length=50)
    hours = forms.CharField(label='Operating Hours', max_length=100)
    doctor_id = forms.CharField(required=False)
    password = forms.CharField(widget=forms.PasswordInput)
    confirm_password = forms.CharField(widget=forms.PasswordInput)
