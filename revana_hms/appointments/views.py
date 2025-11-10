from datetime import datetime
from django.db.models import Q
from django.core.mail import send_mail
from rest_framework import viewsets, permissions
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated

from core.permissions import IsSuperAdmin, IsHospitalAdminOfSameHospital, IsSelfDoctor
from appointments.models import Appointment, DoctorAvailability
from appointments.serializers import AppointmentSerializer, DoctorAvailabilitySerializer
from doctors.models import Doctor

class IsHospitalAdminOrReadOnly(permissions.BasePermission):
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
        user = self.request.user
        department = self.request.query_params.get('department')

        qs = super().get_queryset()

        if hasattr(user, 'patient') and department:
            qs = qs.filter(doctor__department__name__icontains=department)
        elif hasattr(user, 'doctor'):
            qs = qs.filter(doctor=user.doctor)
        elif hasattr(user, 'hospital_admin'):
            qs = qs.filter(doctor__hospital=user.hospital_admin.hospital)
        elif user.is_superuser:
            return qs

        return qs.none()

    def perform_create(self, serializer):
        doctor = serializer.validated_data['doctor']
        date = serializer.validated_data['date']
        start = serializer.validated_data['start_time']
        end = serializer.validated_data['end_time']

        if start >= end:
            raise ValueError("Start time must be before end time.")

        overlap = DoctorAvailability.objects.filter(
            doctor=doctor, date=date
        ).filter(
            Q(start_time__lt=end) & Q(end_time__gt=start)
        ).exists()

        if overlap:
            raise ValueError("Overlapping availability for this doctor on the given date.")

        serializer.save()

class AppointmentViewSet(viewsets.ModelViewSet):
    queryset = Appointment.objects.all()
    serializer_class = AppointmentSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Appointment.objects.filter(patient=self.request.user.patient)

    def perform_create(self, serializer):
        appointment = serializer.save(patient=self.request.user.patient)

        patient_email = self.request.user.email
        doctor_name = appointment.availability.doctor.user.get_full_name()
        date = appointment.availability.date
        time = f"{appointment.availability.start_time} - {appointment.availability.end_time}"

        send_mail(
            subject='Appointment Confirmation',
            message=f'Your appointment with Dr. {doctor_name} on {date} at {time} is confirmed.',
            from_email='your_email@gmail.com',
            recipient_list=[patient_email],
            fail_silently=False,
        )

class CalendarView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user
        start_date = request.query_params.get('start')
        end_date = request.query_params.get('end')
        events = []

        availability_qs = DoctorAvailability.objects.all()
        appointment_qs = Appointment.objects.all()

        if start_date and end_date:
            availability_qs = availability_qs.filter(date__range=[start_date, end_date])
            appointment_qs = appointment_qs.filter(availability__date__range=[start_date, end_date])

        if hasattr(user, 'doctor'):
            availability_qs = availability_qs.filter(doctor=user.doctor)
            appointment_qs = appointment_qs.filter(availability__doctor=user.doctor)

        elif hasattr(user, 'patient'):
            appointment_qs = appointment_qs.filter(patient=user.patient)

        for slot in availability_qs:
            events.append({
                "title": "Available",
                "start": f"{slot.date}T{slot.start_time}",
                "end": f"{slot.date}T{slot.end_time}",
                "color": "#28a745"
            })

        for appt in appointment_qs:
            if hasattr(user, 'doctor'):
                title = f"Booked: {appt.patient.user.get_full_name()}"
                color = "#dc3545"
            else:
                title = f"Your Appointment with Dr. {appt.availability.doctor.user.get_full_name()}"
                color = "#007bff"

            events.append({
                "title": title,
                "start": f"{appt.availability.date}T{appt.availability.start_time}",
                "end": f"{appt.availability.date}T{appt.availability.end_time}",
                "color": color
            })

        return Response(events)

class MobileBookingView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        availability_id = request.data.get('availability_id')
        try:
            slot = DoctorAvailability.objects.get(id=availability_id, is_available=True)
        except DoctorAvailability.DoesNotExist:
            return Response({"error": "Slot not available"}, status=400)

        appointment = Appointment.objects.create(
            patient=request.user.patient,
            availability=slot
        )
        slot.is_available = False
        slot.save()

        return Response({
            "message": "Appointment booked",
            "doctor": slot.doctor.user.get_full_name(),
            "date": slot.date,
            "start": slot.start_time,
            "end": slot.end_time
        })

class MyAppointmentsViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = AppointmentSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Appointment.objects.filter(patient=self.request.user.patient)
