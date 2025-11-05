from rest_framework import permissions
from hospitals.models import HospitalAdmin
from doctors.models import Doctor

class IsSuperAdmin(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user and request.user.is_superuser


class IsHospitalAdminOfSameHospital(permissions.BasePermission):
    """
    Allow hospital admins to manage only their hospital’s doctors, departments, treatments, availability.
    """
    def has_object_permission(self, request, view, obj):
        try:
            hospital_admin = request.user.hospital_admin
        except HospitalAdmin.DoesNotExist:
            return False

        # Doctor object
        if isinstance(obj, Doctor):
            return obj.hospital == hospital_admin.hospital

        # Department/Treatment/Availability objects
        if hasattr(obj, "hospital"):
            return obj.hospital == hospital_admin.hospital

        return False
    

class IsSelfDoctor(permissions.BasePermission):
    """
    Allow doctors to access/modify only their own profile.
    """
    def has_object_permission(self, request, view, obj):
        return hasattr(request.user, 'doctor') and obj == request.user.doctor
    