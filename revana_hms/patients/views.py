from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from .models import Patient
from .serializers import PatientSerializer

class PatientViewSet(viewsets.ModelViewSet):
    queryset = Patient.objects.all()
    serializer_class = PatientSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        if hasattr(user, 'hospitaladmin'):
            return Patient.objects.filter(hospital=user.hospitaladmin.hospital)
        elif hasattr(user, 'doctor'):
            return Patient.objects.filter(hospital=user.doctor.hospital)
        elif hasattr(user, 'patient'):
            return Patient.objects.filter(user=user)
        return Patient.objects.none()
