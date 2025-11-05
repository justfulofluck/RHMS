from django.db import models
#from django.contrib.auth.models import User
from django.conf import settings
from hospitals.models import Hospital, Department, Treatment

User = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)


class Doctor(models.Model):
    STATUS_PENDING = 'pending'
    STATUS_APPROVED = 'approved'
    STATUS_REJECTED = 'rejected'
    STATUS_CHOICES = [
        (STATUS_PENDING, 'Pending'),
        (STATUS_APPROVED, 'Approved'),
        (STATUS_REJECTED, 'Rejected'),
    ]
    
    hospital = models.ForeignKey(Hospital, on_delete=models.CASCADE, related_name="doctors")
    department = models.ForeignKey(Department, on_delete=models.SET_NULL, null=True, blank=True)
    treatment = models.ForeignKey(Treatment, on_delete=models.SET_NULL, null=True, blank=True)
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True, blank=True)

    # Personal details
    name = models.CharField(max_length=150)
    gender = models.CharField(max_length=10, choices=[("Male","Male"),("Female","Female"),("Other","Other")])
    birth_date = models.DateField()
    email = models.EmailField(unique=True)
    contact_number = models.CharField(max_length=15)
    address = models.TextField()

    # Professional details
    registration_number = models.CharField(max_length=50, unique=True)
    medical_certificate = models.FileField(upload_to="doctor_docs/medical_certificates/")
    qualification = models.CharField(max_length=200)
    specialization = models.CharField(max_length=200)
    years_of_experience = models.PositiveIntegerField(default=0)
    designation = models.CharField(
        max_length=50,
        choices=[("Consultant", "Consultant"), ("Resident", "Resident"), ("Surgeon", "Surgeon")]
    )
    # Document uploads
    registration_certificate = models.FileField(upload_to="doctor_docs/registration_certificates/")
    degree_certificates = models.FileField(upload_to="doctor_docs/degree_certificates/")
    aadhaar = models.FileField(upload_to="doctor_docs/aadhaar/")
    passport_photo = models.ImageField(upload_to="doctor_docs/passport_photos/")
    experience_certificate = models.FileField(upload_to="doctor_docs/experience_certificates/", null=True, blank=True)

    # Verification workflow
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default=STATUS_PENDING)
    is_verified = models.BooleanField(default=False)  # optional, can be derived from status
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.name} ({self.specialization})"
