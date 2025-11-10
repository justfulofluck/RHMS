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
    class Meta:
        model = Appointment
        fields = ['id', 'availability', 'booked_at']

    def validate_availability(self, value):
        if not value.is_available:
            raise serializers.ValidationError("This slot is already booked.")
        return value

    def create(self, validated_data):
        availability = validated_data['availability']
        availability.is_available = False
        availability.save()
        return super().create(validated_data)

# class AppointmentSerializer(serializers.ModelSerializer):
#     doctor_name = serializers.CharField(source='doctor.name', read_only=True)
#     hospital_name = serializers.CharField(source='hospital.name', read_only=True)

#     class Meta:
#         model = Appointment
#         fields = [
#             'id', 'hospital', 'hospital_name', 'doctor', 'doctor_name',
#             'patient_name', 'appointment_date', 'status'
#         ]
#         read_only_fields = ['status']

#     def validate(self, data):
#         # Ensure doctor belongs to the hospital
#         doctor: Doctor = data['doctor']
#         hospital: Hospital = data['hospital']
#         if doctor.hospital_id != hospital.id:
#             raise serializers.ValidationError("Selected doctor does not belong to the chosen hospital.")

#         # Optional: ensure appointment falls within an availability slot
#         # You can tighten this rule later (exact slot match vs. within range)

#         return data
