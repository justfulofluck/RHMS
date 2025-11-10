from rest_framework import viewsets, permissions, decorators, response, status
from .models import Doctor, DoctorAvailability
from .serializers import DoctorSerializer, DoctorAvailabilitySerializer


class DoctorAvailabilityViewSet(viewsets.ModelViewSet):
    queryset = DoctorAvailability.objects.all()
    serializer_class = DoctorAvailabilitySerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        if hasattr(user, 'doctor'):
            return DoctorAvailability.objects.filter(doctor=user.doctor)
        return DoctorAvailability.objects.none()

    def perform_create(self, serializer):
        serializer.save(doctor=self.request.user.doctor)


class DoctorViewSet(viewsets.ModelViewSet):
    queryset = Doctor.objects.select_related('hospital', 'department', 'treatment').all()
    serializer_class = DoctorSerializer
    permission_classes = [permissions.IsAuthenticated]

    @decorators.action(detail=True, methods=['post'])
    def approve(self, request, pk=None):
        doctor = self.get_object()
        serializer = self.get_serializer()
        serializer.approve(doctor)
        return response.Response(
            {'status': doctor.status, 'is_verified': doctor.is_verified, 'user_id': doctor.user.id},
            status=status.HTTP_200_OK
        )

    @decorators.action(detail=True, methods=['post'])
    def reject(self, request, pk=None):
        doctor = self.get_object()
        serializer = self.get_serializer()
        serializer.reject(doctor)
        return response.Response(
            {'status': doctor.status, 'is_verified': doctor.is_verified},
            status=status.HTTP_200_OK
        )

    def get_queryset(self):
        qs = super().get_queryset()
        user = self.request.user

        if hasattr(user, 'doctor'):
            return qs.filter(id=user.doctor.id)  # Doctor sees only self
        elif hasattr(user, 'hospital_admin'):
            return qs.filter(hospital=user.hospital_admin.hospital)  # Hospital admin sees own hospital
        elif user.is_superuser:
            return qs  # Super admin sees all
        return qs.none()


class PublicAvailabilityViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = DoctorAvailability.objects.filter(is_available=True)
    serializer_class = DoctorAvailabilitySerializer
    permission_classes = [permissions.AllowAny]