from rest_framework import serializers
from django.contrib.auth.models import User
from .models import Doctor, DoctorAvailability


class DoctorAvailabilitySerializer(serializers.ModelSerializer):
    class Meta:
        model = DoctorAvailability
        fields = ['id', 'date', 'start_time', 'end_time', 'is_available']

    def validate(self, data):
        doctor = self.context['request'].user.doctor
        date = data['date']
        start = data['stat_time']
        end = data['end_time']

        #time range validation
        if start >= end:
            raise serializers.ValidationError("Start time must be before end Time")
        

        #slot Conflit

        conflicts = DoctorAvailability.objects.filter(
            doctor=doctor,
            data=date,
            start_time__lt=end,
            end_time_gt=start
        )
        if self.instance:
            conflicts = conflicts.exclude(id=self.instance.id)
        
        if conflicts.exists():
            raise serializers.ValidationError("This slot overlaps with an existing availability")
        
        return data

class DoctorSerializer(serializers.ModelSerializer):
    # Mapped fields from User and DoctorProfile
    email = serializers.EmailField(source='user.email', read_only=True)
    
    # Profile fields (Read-Only for now as write logic is custom in views)
    gender = serializers.CharField(source='user.doctorprofile.gender', read_only=True)
    birth_date = serializers.DateField(source='user.doctorprofile.date_of_birth', read_only=True)
    contact_number = serializers.CharField(source='user.doctorprofile.contact_number', read_only=True)
    address = serializers.CharField(source='user.doctorprofile.address', read_only=True)
    qualification = serializers.CharField(source='user.doctorprofile.qualification', read_only=True)
    years_of_experience = serializers.IntegerField(source='user.doctorprofile.year_of_experience', read_only=True)
    aadhaar = serializers.CharField(source='user.doctorprofile.aadhaar', read_only=True)
    
    # File fields
    medical_certificate = serializers.FileField(source='user.doctorprofile.medical_certificate', read_only=True)
    registration_certificate = serializers.FileField(source='user.doctorprofile.registration_certificate', read_only=True)
    degree_certificates = serializers.FileField(source='user.doctorprofile.degree_certificates', read_only=True)
    passport_photo = serializers.ImageField(source='user.doctorprofile.passport_photo', read_only=True)
    experience_certificate = serializers.FileField(source='user.doctorprofile.experience_certificate', read_only=True)

    class Meta:
        model = Doctor
        fields = [
            'id', 'hospital', 'department', 'treatments',
            'name', 'gender', 'birth_date', 'email', 'contact_number', 'address',
            'medical_certificate', 'qualification',
            'specialization', 'years_of_experience',
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
        
        # Assign role and activate user
        doctor.user.role = 'doctor'
        doctor.user.is_active = True
        doctor.user.save()
        
        doctor.save()
        return doctor

    def reject(self, doctor: Doctor):
        doctor.status = Doctor.STATUS_REJECTED
        doctor.is_verified = False
        doctor.save()
        return doctor
