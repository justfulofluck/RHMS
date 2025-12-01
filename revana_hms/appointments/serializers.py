from rest_framework import serializers
from .models import Appointment, DoctorAvailability
from doctors.models import Doctor
from hospitals.models import Hospital

class DoctorAvailabilitySerializer(serializers.ModelSerializer):
    doctor_name = serializers.CharField(source='doctor.name', read_only=True)

    class Meta:
        model = DoctorAvailability
        fields = ['id', 'doctor', 'doctor_name', 'date', 'start_time', 'end_time', 'is_available']



class AppointmentSerializer(serializers.ModelSerializer):
    doctor_name = serializers.CharField(source='doctor.name', read_only=True)
    hospital_name = serializers.CharField(source='hospital.name', read_only=True)

    class Meta:
        model = Appointment
        fields = ['id', 'hospital', 'hospital_name', 'doctor', 'doctor_name', 'patient_name', 'appointment_date', 'created_at']
        read_only_fields = ['created_at']