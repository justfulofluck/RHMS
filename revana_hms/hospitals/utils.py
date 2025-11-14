import random, string
from django.contrib.auth.models import User
from django.core.mail import send_mail
from django.contrib.auth.hashers import make_password
from .models import Hospital, HospitalAdmin

def approve_hospital(hospital_id):
    hospital = Hospital.objects.get(id=hospital_id)
    hospital.status = Hospital.STATUS_APPROVED
    hospital.save()

    # Generate random password
    password = ''.join(random.choices(string.ascii_letters + string.digits, k=10))

    # Create user
    user = User.objects.create(
        username=hospital.email,
        email=hospital.email,
        password=make_password(password)
    )

    # Link hospital admin
    HospitalAdmin.objects.create(user=user, hospital=hospital)

    # Send email
    send_mail(
        subject="Hospital Registration Approved",
        message=f"Your hospital has been approved!\n\nLogin details:\nUsername: {hospital.email}\nPassword: {password}\nDashboard: http://127.0.0.1:8000/hospital/dashboard/",
        from_email="admin@revana.com",
        recipient_list=[hospital.email],
        fail_silently=False,
    )
