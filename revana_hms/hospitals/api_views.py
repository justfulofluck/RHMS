from rest_framework import status, permissions
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.generics import ListAPIView
import secrets
from django.core.mail import send_mail
from django.contrib.auth import get_user_model
from .models import Hospital, HospitalAdmin
from .serializers import HospitalRegisterSerializer, HospitalPublicSerializer

User = get_user_model()

class HospitalRegisterAPI(APIView):
    """
    Public endpoint to register a hospital.
    Saves hospital with status = pending.
    """
    permission_classes = [permissions.AllowAny]

    def post(self, request):
        serializer = HospitalRegisterSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        hospital = serializer.save()  # status defaults to 'pending'
        return Response(
            {"message": "Hospital submitted for approval", "hospitalId": hospital.id},
            status=status.HTTP_201_CREATED
        )


class HospitalListAPI(ListAPIView):
    """
    Public endpoint to list approved hospitals.
    """
    permission_classes = [permissions.AllowAny]
    serializer_class = HospitalPublicSerializer

    def get_queryset(self):
        return Hospital.objects.filter(status=Hospital.STATUS_APPROVED).order_by("name")


class ApproveHospitalAPI(APIView):
    permission_classes = [permissions.IsAdminUser]  # only superusers/staff

    def post(self, request, hospital_id):
        try:
            hospital = Hospital.objects.get(id=hospital_id, status=Hospital.STATUS_PENDING)
        except Hospital.DoesNotExist:
            return Response({'error': 'Hospital not found or not pending'}, status=status.HTTP_404_NOT_FOUND)

        # Approve hospital
        hospital.status = Hospital.STATUS_APPROVED
        hospital.save()

        # Create hospital admin user
        user, created = User.objects.get_or_create(
            username=hospital.email,
            defaults={'email': hospital.email, 'is_staff': True, 'is_superuser': False}
        )
        password = secrets.token_urlsafe(10)
        user.set_password(password)
        user.save()

        HospitalAdmin.objects.get_or_create(user=user, hospital=hospital)

        # Send email
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
