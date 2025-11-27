from django.db import models
from django.conf import settings
from accounts.models import User
from hospitals.models import Hospital, Department, Treatment


class Doctor(models.Model):
    STATUS_PENDING = 'pending'
    STATUS_APPROVED = 'approved'
    STATUS_REJECTED = 'rejected'
    STATUS_CHOICES = [
        (STATUS_PENDING, 'Pending'),
        (STATUS_APPROVED, 'Approved'),
        (STATUS_REJECTED, 'Rejected'),
    ]

    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, default=1)
    specialization = models.CharField(max_length=100)
    hospital = models.ForeignKey('hospitals.Hospital', on_delete=models.CASCADE, default=1)
    department = models.ForeignKey(Department, on_delete=models.SET_NULL, null=True, blank=True, related_name='doctors')
    treatments = models.ManyToManyField(Treatment, blank=True, related_name='doctors')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default=STATUS_PENDING)
    is_approved = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.user.email} - {self.specialization}"


class DoctorAvailability(models.Model):
    doctor = models.ForeignKey(User, on_delete=models.CASCADE, limit_choices_to={'role': 'doctor'})
    date = models.DateField()
    start_time = models.TextField()
    end_time = models.TimeField()
    is_available = models.BooleanField(default=True)

    class MetaL:
        unique_together = ('doctor', 'date', 'start_time', 'end_time')

    def __str__(self):
        return f"{self.doctor.username} - {self.date} ({self.start_time} to {self.end_time})"






