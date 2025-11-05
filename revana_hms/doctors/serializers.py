from rest_framework import serializers
from django.contrib.auth.models import User
from .models import Doctor


class DoctorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Doctor
        fields = [
            'id', 'hospital', 'department', 'treatment',
            'name', 'gender', 'birth_date', 'email', 'contact_number', 'address',
            'registration_number', 'medical_certificate', 'qualification',
            'specialization', 'years_of_experience', 'designation',
            'registration_certificate', 'degree_certificates', 'aadhaar',
            'passport_photo', 'experience_certificate',
            'status', 'is_verified', 'user', 'created_at'
        ]
        read_only_fields = ['status', 'is_verified', 'user', 'created_at']

    def create(self, validated_data):
        # New doctors always start as pending
        validated_data['status'] = Doctor.STATUS_PENDING
        validated_data['is_verified'] = False
        return super().create(validated_data)

    def approve(self, doctor: Doctor):
        """Approve doctor and auto-create User if not exists"""
        if not doctor.user:
            user = User.objects.create_user(
                username=doctor.email,
                email=doctor.email,
                password=User.objects.make_random_password(),
                first_name=doctor.name
            )
            doctor.user = user
        doctor.status = Doctor.STATUS_APPROVED
        doctor.is_verified = True
        doctor.save()
        return doctor

    def reject(self, doctor: Doctor):
        doctor.status = Doctor.STATUS_REJECTED
        doctor.is_verified = False
        doctor.save()
        return doctor
