from django.db import models
from hospitals.models import Hospital
from doctors.models import Doctor


class DoctorAvailability(models.Model):
    doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE, related_name='availabilities')
    date = models.DateField()
    start_time = models.TimeField()
    end_time = models.TimeField()
    is_available = models.BooleanField(default=True)

    class Meta:
        db_table = 'rhms_doctor_availabilities'
        unique_together = ('doctor', 'date', 'start_time', 'end_time')

    def __str__(self):
        return f'{self.doctor.name} - {self.date} {self.start_time}-{self.end_time}'

class Patient(models.Model):
    name = models.CharField(max_length=255)
    age = models.IntegerField()
    gender = models.CharField(max_length=10)
    contact_number = models.CharField(max_length=15)
    address = models.TextField()

class Appointment(models.Model):
    hospital = models.ForeignKey(Hospital, on_delete=models.CASCADE, related_name="appointments")
    doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE, related_name="appointments")
    patient_name = models.CharField(max_length=150)
    appointment_date = models.DateTimeField()
    status = models.CharField(
        max_length=20,
        choices=[("Pending", "Pending"), ("Confirmed", "Confirmed"), ("Cancelled", "Cancelled")],
        default="Pending"
    )

    def __str__(self):
        return f"Appointment with {self.doctor.name} on {self.appointment_date}"