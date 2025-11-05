from django.db import models
from accounts.models import User  # or wherever your User model is
from hospitals.models import Hospital
from accounts.models import User


class Patient(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    hospital = models.ForeignKey(Hospital, on_delete=models.CASCADE)
    age = models.PositiveIntegerField()
    gender = models.CharField(max_length=10, choices=[('male', 'Male'), ('female', 'Female'), ('other', 'Other')])
    phone = models.CharField(max_length=15)
    address = models.TextField()
    medical_history = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"{self.user.get_full_name()} ({self.hospital.name})"
