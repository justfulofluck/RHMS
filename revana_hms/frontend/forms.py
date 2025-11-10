from django import forms

class HospitalRegistrationForm(forms.Form):
    name = forms.CharField()
    registration_number = forms.CharField()
    email = forms.EmailField()
    phone_number = forms.CharField()
    address = forms.CharField(widget=forms.Textarea)
    city = forms.CharField()
    state = forms.CharField()
    country = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput)
    confirm_password = forms.CharField(widget=forms.PasswordInput)

    def clean(self):
        cleaned_data = super().clean()
        if cleaned_data.get('password') != cleaned_data.get('confirm_password'):
            raise forms.ValidationError("Passwords do not match.")
        return cleaned_data
