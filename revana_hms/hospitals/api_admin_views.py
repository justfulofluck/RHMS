from rest_framework import status, permissions
from rest_framework.response import Response
from rest_framework.views import APIView
from django.core.mail import send_mail
from django.contrib.auth import get_user_model
import secrets
from .models import Hospital, HospitalAdmin

User = get_user_model()


class IsSuperAdmin(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.is_superuser


class ApprovalHospitalAPI(APIView):
    permission_classes = [IsSuperAdmin]

    def post(self, request, hospital_id):
        try:
            hospital = Hospital.objects.get(id=hospital_id, status=Hospital.STATUS_PENDING)
        except Hospital.DoesNotExist:
            return Response(
                {'error': 'Hospital not found or already processed.'},
                status=status.HTTP_404_NOT_FOUND
            )

        # Approve hospital
        hospital.status = Hospital.STATUS_APPROVED
        hospital.save()

        # Create or update hospital admin user
        user, created = User.objects.get_or_create(
            username=hospital.email,
            defaults={
                'email': hospital.email,
                'is_staff': True,
                'is_superuser': False,
            }
        )
        password = secrets.token_urlsafe(10)
        user.set_password(password)
        user.save()

        HospitalAdmin.objects.update_or_create(user=user, hospital=hospital)

        # Send email with credentials
        send_mail(
            subject='Hospital Approved',
            message=(
                f'Dear {hospital.name},\n\n'
                f'Your hospital has been approved.\n'
                f'Login: /admin/\n'
                f'Username: {hospital.email}\n'
                f'Password: {password}\n'
            ),
            from_email=None,
            recipient_list=[hospital.email],
        )

        return Response({'message': 'Hospital approved and credentials sent'})
