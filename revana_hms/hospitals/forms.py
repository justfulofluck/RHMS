from django import forms
from django.core.validators import RegexValidator
from django.contrib.auth.models import User
from hospitals.models import Hospital

HOSPITAL_TYPES = [
    ('general', 'General'),
    ('multispeciality', 'Multispeciality'),
]

class Meta:
    model = Hospital
    fields = [
        'name', 'logo', 'registration_number', 'email', 'contact_number',
        'address', 'city', 'state', 'country', 'hospital_type', 'hours'
    ]
    widgets = {
        'password': forms.PasswordInput(),
    }

def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get("password")
        confirm_password = cleaned_data.get("confirm_password")
        if password and confirm_password and password != confirm_password:
            self.add_error('confirm_password', "Passwords do not match.")

class HospitalRegistrationForm(forms.Form):
    name = forms.CharField(label='Hospital Name', max_length=100)
    logo = forms.ImageField(required=False)
    registration_number = forms.CharField(label='Registration Number', max_length=50, required=True)
    email = forms.EmailField(label='Email')
    contact_number = forms.CharField(
        widget=forms.NumberInput(attrs={'class': ' form-control'}),
        validators=[RegexValidator(r'^\d{10}$', 'Enter a valid 10-digit number')]
    )
    address = forms.CharField(widget=forms.Textarea)
    city = forms.CharField(max_length=50)
    state = forms.CharField(max_length=50)
    country = forms.CharField(max_length=50)
    hospital_type = forms.ChoiceField(
        choices=HOSPITAL_TYPES,
        widget=forms.Select(attrs={'class': 'from-select'})
    )
    hours = forms.CharField(label='Operating Hours', max_length=100)
    doctor_id = forms.CharField(required=False)
    password = forms.CharField(widget=forms.PasswordInput)
    confirm_password = forms.CharField(widget=forms.PasswordInput)

