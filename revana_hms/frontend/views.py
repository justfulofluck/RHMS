from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import get_user_model
from hospitals.models import Hospital
from .forms import HospitalRegistrationForm

User = get_user_model()

def register_hospital(request):
    if request.method == 'POST':
        form = HospitalRegistrationForm(request.POST)
        if form.is_valid():
            data = form.cleaned_data

            if User.objects.filter(email=data['email']).exists():
                messages.error(request, "Email already registered.")
                return redirect('register_hospital')
            if User.objects.filter(phone=data['phone_number']).exists():
                messages.error(request, "Phone number already registered.")
                return redirect('register_hospital')

            user = User.objects.create_user(
                username=data['email'],
                email=data['email'],
                password=data['password'],
                phone=data['phone_number'],
                role='hospital_admin'
            )

            Hospital.objects.create(
                name=data['name'],
                registration_number=data['registration_number'],
                email=data['email'],
                phone_number=data['phone_number'],
                address=data['address'],
                city=data['city'],
                state=data['state'],
                country=data['country'],
                admin=user
            )

            messages.success(request, "Hospital registered successfully.")
            return redirect('register_hospital')
        else:
            messages.error(request, "Please correct the errors below.")
    else:
        form = HospitalRegistrationForm()

    return render(request, 'frontend/register_hospital.html', {'form': form})
