from datetime import datetime
from rest_framework import viewsets, permissions
from rest_framework.decorators import action
from rest_framework.response import Response
from django.db.models import Q
from core.permissions import IsSuperAdmin, IsHospitalAdminOfSameHospital, IsSelfDoctor
from .models import Appointment, DoctorAvailability
from .serializers import AppointmentSerializer, DoctorAvailabilitySerializer
from doctors.models import Doctor
from appointments.models import Appointment, DoctorAvailability
from appointments.serializers import AppointmentSerializer

class IsHospitalAdminOrReadOnly(permissions.BasePermission):
    """
    Allow safe reads; restrict writes to authenticated users.
    Replace/extend with your role checks (super admin / hospital admin).
    """
    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return True
        return request.user and request.user.is_authenticated


class DoctorAvailabilityViewSet(viewsets.ModelViewSet):
    queryset = DoctorAvailability.objects.select_related('doctor').all()
    serializer_class = DoctorAvailabilitySerializer
    permission_classes = [IsHospitalAdminOrReadOnly]

    def get_permissions(self):
        if self.action in ['create', 'update', 'partial_update', 'destroy']:
            return [permissions.IsAuthenticated(), IsSuperAdmin() | IsHospitalAdminOfSameHospital() | IsSelfDoctor()]
        return [permissions.IsAuthenticated()]


    def get_queryset(self):
        qs = super().get_queryset()
        user = self.request.user

        if hasattr(user, 'doctor'):
            return qs.filter(doctor=user.doctor)
        elif hasattr(user, 'hospital_admin'):
            return qs.filter(doctor__hospital=user.hospital_admin.hospital)
        elif user.is_superuser:
            return qs
        return qs.none()

    def perform_create(self, serializer):
        # Optional: enforce no overlapping availability blocks for the same doctor
        doctor = serializer.validated_data['doctor']
        date = serializer.validated_data['date']
        start = serializer.validated_data['start_time']
        end = serializer.validated_data['end_time']

        overlap = DoctorAvailability.objects.filter(
            doctor=doctor, date=date
        ).filter(
            Q(start_time__lt=end) & Q(end_time__gt=start)
        ).exists()

        if overlap:
            raise ValueError("Overlapping availability for this doctor on the given date.")

        serializer.save()


class AppointmentViewSet(viewsets.ModelViewSet):
    queryset = Appointment.objects.select_related('hospital', 'doctor').all()
    serializer_class = AppointmentSerializer
    permission_classes = [IsHospitalAdminOrReadOnly]

    def get_queryset(self):
        qs = super().get_queryset()
        user = self.request.user

        if hasattr(user, 'doctor'):
            return qs.filter(doctor=user.doctor)
        elif hasattr(user, 'hospital_admin'):
            return qs.filter(doctor__hospital=user.hospital_admin.hospital)
        elif user.is_superuser:
            return qs
        return qs.none()


    def get_queryset(self):
        qs = super().get_queryset()
        hospital_id = self.request.query_params.get('hospital')
        doctor_id = self.request.query_params.get('doctor')
        date = self.request.query_params.get('date')
        status = self.request.query_params.get('status')

        if hospital_id:
            qs = qs.filter(hospital_id=hospital_id)
        if doctor_id:
            qs = qs.filter(doctor_id=doctor_id)
        if status:
            qs = qs.filter(status=status)
        if date:
            # Filter by date part of appointment_date
            qs = qs.filter(appointment_date__date=date)
        return qs

    @action(detail=True, methods=['post'])
    def confirm(self, request, pk=None):
        appt = self.get_object()
        appt.status = "Confirmed"
        appt.save(update_fields=['status'])
        return Response({'status': appt.status})

    @action(detail=True, methods=['post'])
    def cancel(self, request, pk=None):
        appt = self.get_object()
        appt.status = "Cancelled"
        appt.save(update_fields=['status'])
        return Response({'status': appt.status})

class MyAppointmentsViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = AppointmentSerializer
    permission_classes = [permissions.IsAuthenticated, IsSelfDoctor]

    def get_queryset(self):
        return Appointment.objects.filter(doctor=self.request.user.doctor)


