from django.db import models
from django.utils import timezone  # ✅ Required for created_at default
from hospitals.models import Hospital
from doctors.models import Doctor


class DoctorAvailability(models.Model):
    doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE, related_name='availabilities')
    date = models.DateField()
    start_time = models.TimeField()
    end_time = models.TimeField()
    is_available = models.BooleanField(default=True)
    
    # Slot duration in minutes
    slot_duration = models.IntegerField(
        default=30,
        choices=[
            (15, '15 minutes'),
            (30, '30 minutes'),
            (45, '45 minutes'),
            (60, '60 minutes'),
        ],
        help_text="Duration of each appointment slot in minutes"
    )

    class Meta:
        db_table = 'rhms_doctor_availabilities'
        unique_together = ('doctor', 'date', 'start_time', 'end_time')

    def __str__(self):
        return f'{self.doctor.name} - {self.date} {self.start_time}-{self.end_time}'


from django.conf import settings




# class Appointment(models.Model):
#     hospital = models.ForeignKey(Hospital, on_delete=models.CASCADE, related_name="appointments")
#     doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE, related_name="appointments")
#     patient_name = models.CharField(max_length=150)
#     appointment_date = models.DateTimeField()
#     status = models.CharField(
#         max_length=20,
#         choices=[("Pending", "Pending"), ("Confirmed", "Confirmed"), ("Cancelled", "Cancelled")],
#         default="Pending"
#     )
#     created_at = models.DateTimeField(default=timezone.now)  # ✅ Now works correctly

#     def __str__(self):
#         return f"Appointment with {self.doctor.name} on {self.appointment_date}"

class Appointment(models.Model):
    STATUS_CHOICES = [
        ('scheduled', 'Scheduled'),
        ('confirmed', 'Confirmed'),
        ('completed', 'Completed'),
        ('cancelled', 'Cancelled'),
        ('no_show', 'No Show'),
    ]

    hospital = models.ForeignKey(Hospital, on_delete=models.CASCADE, related_name="appointments")
    doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE, related_name="appointments")
    patient_name = models.CharField(max_length=150)
    appointment_date = models.DateTimeField()
    token_number = models.PositiveIntegerField(null=True, blank=True)
    created_at = models.DateTimeField(default=timezone.now)
    
    # Status Tracking
    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='scheduled'
    )
    notes = models.TextField(blank=True, null=True)
    cancelled_at = models.DateTimeField(null=True, blank=True)
    cancellation_reason = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"Appointment with {self.doctor.name} on {self.appointment_date}"
        