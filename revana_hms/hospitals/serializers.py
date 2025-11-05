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
    class Meta:
        model = Hospital
        fields = ["id", "name", "city", "logo"]

class DepartmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Department
        fields = ['id', 'hospital', 'name', 'description']

class TreatmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Treatment
        fields = ['id', 'hospital', 'department', 'name', 'description']

