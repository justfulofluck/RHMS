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
    # Safe Profile Access
    def get_profile_attr(self, obj, attr):
        if hasattr(obj.user, 'doctorprofile'):
            return getattr(obj.user.doctorprofile, attr, None)
        return None

    # email = serializers.EmailField(source='user.email', read_only=True)

    gender = serializers.SerializerMethodField()
    def get_gender(self, obj): return self.get_profile_attr(obj, 'gender')

    birth_date = serializers.SerializerMethodField()
    def get_birth_date(self, obj): return self.get_profile_attr(obj, 'date_of_birth')

    contact_number = serializers.SerializerMethodField()
    def get_contact_number(self, obj): return self.get_profile_attr(obj, 'contact_number')

    address = serializers.SerializerMethodField()
    def get_address(self, obj): return self.get_profile_attr(obj, 'address')

    qualification = serializers.SerializerMethodField()
    def get_qualification(self, obj): return self.get_profile_attr(obj, 'qualification')

    years_of_experience = serializers.SerializerMethodField()
    def get_years_of_experience(self, obj): return self.get_profile_attr(obj, 'year_of_experience')

    aadhaar = serializers.SerializerMethodField()
    def get_aadhaar(self, obj): return self.get_profile_attr(obj, 'aadhaar')

    # File fields - Need to return URL if exists
    def get_file_url(self, obj, attr):
        if hasattr(obj.user, 'doctorprofile'):
            file_field = getattr(obj.user.doctorprofile, attr, None)
            if file_field:
                return file_field.url
        return None

    medical_certificate = serializers.SerializerMethodField()
    def get_medical_certificate(self, obj): return self.get_file_url(obj, 'medical_certificate')

    registration_certificate = serializers.SerializerMethodField()
    def get_registration_certificate(self, obj): return self.get_file_url(obj, 'registration_certificate')

    degree_certificates = serializers.SerializerMethodField()
    def get_degree_certificates(self, obj): return self.get_file_url(obj, 'degree_certificates')

    passport_photo = serializers.SerializerMethodField()
    def get_passport_photo(self, obj): return self.get_file_url(obj, 'passport_photo')

    experience_certificate = serializers.SerializerMethodField()
    def get_experience_certificate(self, obj): return self.get_file_url(obj, 'experience_certificate')

    class Meta:
        model = Doctor
        fields = [
            'id', 'hospital', 'department', 'treatments',
            'name', 'gender', 'birth_date', 'contact_number', 'address',
            'medical_certificate', 'qualification',
            'specialization', 'years_of_experience',
            'registration_certificate', 'degree_certificates', 'aadhaar',
            'passport_photo', 'experience_certificate',
            'status', 'is_approved', 'user'
        ]
        read_only_fields = ['status', 'is_approved', 'user']

    def create(self, validated_data):
        # New doctors always start as pending
        validated_data['status'] = Doctor.STATUS_PENDING
        validated_data['is_approved'] = False
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
        doctor.is_approved = True
        
        # Assign role and activate user
        doctor.user.role = 'doctor'
        doctor.user.is_active = True
        doctor.user.save()
        
        doctor.save()
        return doctor

    def reject(self, doctor: Doctor):
        doctor.status = Doctor.STATUS_REJECTED
        doctor.is_approved = False
        doctor.save()
        return doctor
