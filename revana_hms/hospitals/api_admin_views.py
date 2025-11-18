# hospitals/api_admin_views.py
from rest_framework import status, permissions
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import Hospital
from .utils import approve_hospital_and_notify


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

        # Approve and save
        hospital.status = Hospital.STATUS_APPROVED
        hospital.save()

        # Notify (creates user, links admin, sends email)
        try:
            approve_hospital_and_notify(hospital)
            return Response({'message': 'Hospital approved and credentials sent'}, status=status.HTTP_200_OK)
        except Exception as e:
            # approve_hospital_and_notify itself catches email exceptions,
            # but if something else bubbles up, we handle it here.
            return Response({'message': 'Hospital approved, but notification failed', 'error': str(e)}, status=status.HTTP_200_OK)
