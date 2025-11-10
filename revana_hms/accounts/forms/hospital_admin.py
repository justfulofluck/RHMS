from django import forms
from accounts.models import HospitalAdminProfile, DoctorProfile


class HospitalAdminRegistrationForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)
    confirm_password = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        model = HospitalAdminProfile
        fields = [
            'name', 
            'registration_number', 
            'contact_number', 
            #'email', 
            'address', 
            'hospital_type', 
            'hours', 
            'doctor_id'
        ]

        def clean(self):
            cleaned_data = super().clean()
            if cleaned_data.get('password') != cleaned_data.get('confirm_password'):
                raise forms.ValidationError("password do not match.")
            return cleaned_data
        
class DoctorRegistrationForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)
    confirm_password = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        model = DoctorProfile
        fields = [
            # Personal Info
            'gender', 
            'date_of_birth', 
            'contact_number', 
            'address',
            
            # Professional Info
            'registration_number', 
            'medical_certificate', 
            'qualification',
            'specialization', 
            'year_of_experience', 
            'designation',
            'department', 
            'timing', 
            'opd_timings', 
            'availability_status',
            # Documents
            'registration_certificate', 
            'degree_certificates', 
            'aadhaar',
            'passport_photo', 
            'experience_certificate'
        ]

    def clean(self):
        cleaned_data = super().clean()
        if cleaned_data.get('password') != cleaned_data.get('confirm_password'):
            raise forms.ValidationError("Passwords do not match.")
        return cleaned_data