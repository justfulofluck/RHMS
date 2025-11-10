from django.db import models
from django.conf import settings
from django.contrib.auth.models import User


class Hospital(models.Model):
    STATUS_PENDING = 'pending'
    STATUS_APPROVED = 'approved'
    STATUS_REJECTED = 'rejected'
    STATUS_CHOICES = [
        (STATUS_PENDING, 'Pending'),
        (STATUS_APPROVED, 'Approved'),
        (STATUS_REJECTED, 'Rejected'),
    ]

    name = models.CharField(max_length=200)
    registration_number = models.CharField(max_length=100, unique=True)
    email = models.EmailField(unique=True)
    logo = models.ImageField(upload_to='hospital_logos/', blank=True, null=True)
    address = models.TextField()
    phone_number = models.CharField(max_length=20)
    city = models.CharField(max_length=100)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default=STATUS_PENDING)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'rhms_hospitals'
    
    def __str__(self):
        return self.name
    

from django.conf import settings

class HospitalAdmin(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, default=1)
    hospital = models.ForeignKey('hospitals.Hospital', on_delete=models.CASCADE, default=1)

    def __str__(self):
        return f"{self.user.get_full_name()} - Admin"

# class HospitalAdmin(models.Model):
#     user = models.OneToOneField(User, on_delete=models.CASCADE)
#     hospital = models.OneToOneField(Hospital, on_delete=models.CASCADE, related_name='admin')

#     class Meta:
#         db_table = 'rhms_hospital_admins'

#     def __str__(self):
#         return f'{self.user.username} -> {self.hospital.name}'
        

class Department(models.Model):
    hospital = models.ForeignKey('hospitals.Hospital', on_delete=models.CASCADE, related_name="departments")
    name = models.CharField(max_length=100)

    def __str__(self):
        return f"{self.name} ({self.hospital.name})"


class Treatment(models.Model):
    hospital = models.ForeignKey('hospitals.Hospital', on_delete=models.CASCADE, related_name="treatments")
    department = models.ForeignKey(Department, on_delete=models.CASCADE, related_name="treatments")
    name = models.CharField(max_length=100)

    def __str__(self):
        return f"{self.name} - {self.department.name} ({self.hospital.name})"

    
# class HospitalAdmin(models.Model):
#     user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="hospital_admin")
#     Hospital = models.OneToOneField("hospital", on_delete=models.CASCADE, related_name="admin")

#     def __str__(self):
#         return f"{self.user.username} - {self.Hospital.name}"
    