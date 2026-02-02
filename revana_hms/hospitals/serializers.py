from rest_framework import serializers
from .models import Hospital, Department, Treatment

class HospitalRegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model = Hospital
        fields = [
            "name",
            "registration_number",
            "email",
            "logo",
            "address",
            "phone_number",
            "city",
        ]


class HospitalPublicSerializer(serializers.ModelSerializer):
    p_number = serializers.CharField(source='phone_number')
    total_doctors = serializers.SerializerMethodField()
    total_departments = serializers.SerializerMethodField()

    class Meta:
        model = Hospital
        fields = ["id", "name", "city", "logo", "hospital_type", "email", "p_number", "address", "total_doctors", "total_departments"]

    def get_total_doctors(self, obj):
        return obj.doctor_set.count()

    def get_total_departments(self, obj):
        return obj.departments.count()

class DepartmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Department
        fields = ['id', 'hospital', 'name']

class TreatmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Treatment
        fields = ['id', 'hospital', 'department', 'name']

