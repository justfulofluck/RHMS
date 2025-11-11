from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, BaseUserManager

# ---------------- Custom User Manager ----------------
class UserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError("Email is required")
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_active', True)

        return self.create_user(email, password, **extra_fields)



# ---------------- Custom User Model ----------------
class User(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(unique=True)
    role = models.CharField(max_length=50)
    phone = models.CharField(max_length=10, blank=True, null=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    objects = UserManager()

    def __str__(self):
        return self.email
    


# ---------------- Hospital Admin Profile ----------------
class HospitalAdminProfile(models.Model):
    user = models.OneToOneField('accounts.User', on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    contact_number = models.CharField(max_length=10)
    registration_number = models.CharField(max_length=100)
    address = models.TextField()
    hospital_type = models.CharField(max_length=100)
    hours = models.CharField(max_length=100)
    doctor_id = models.CharField(max_length=100)

    def __str__(self):
        return self.name

# ---------------- Doctor Profile ----------------
class DoctorProfile(models.Model):
    user = models.OneToOneField('accounts.User', on_delete=models.CASCADE)
    gender = models.CharField(max_length=10)
    date_of_birth = models.DateField()
    contact_number = models.CharField(max_length=15)
    address = models.TextField()
    registration_number = models.CharField(max_length=100)
    medical_certificate = models.FileField(upload_to='certificates/')
    qualification = models.CharField(max_length=255)
    specialization = models.CharField(max_length=255)
    year_of_experience = models.IntegerField()
    designation = models.CharField(max_length=100)
    department = models.CharField(max_length=100)
    timing = models.CharField(max_length=100)
    opd_timings = models.CharField(max_length=100)
    availability_status = models.BooleanField(default=True)
    registration_certificate = models.FileField(upload_to='certificates/')
    degree_certificates = models.FileField(upload_to='certificates/')
    aadhaar = models.FileField(upload_to='documents/')
    passport_photo = models.ImageField(upload_to='photos/')
    experience_certificate = models.FileField(upload_to='certificates/', null=True, blank=True)

    def __str__(self):
        return f"{self.user.email} - {self.specialization}"
