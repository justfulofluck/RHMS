from django.db import models

class Hospital(models.Model):
    name = models.CharField(max_length=200)
    contact_number = models.CharField(max_length=20)
    email = models.EmailField(unique=True)
    address = models.TextField()
    city = models.CharField(max_length=100)
    state = models.CharField(max_length=100)
    country = models.CharField(max_length=100)
    Hospital_type = models.CharField(max_length=100)
    logo = models.ImageField(upload_to='hospital_logos/', blank=True, null=True)
    hours = models.CharField(max_length=100)
    password = models.CharField(max_length=128)

    def __str__(self):
        return self.name
    