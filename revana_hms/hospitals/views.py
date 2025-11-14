from django.shortcuts import render, redirect
from django.urls import reverse
from rest_framework import viewsets, permissions ,decorators, response, status
from doctors.models import Doctor
from .models import Department, Treatment, Hospital
from .serializers import DepartmentSerializer, TreatmentSerializer, HospitalRegisterSerializer
from doctors.serializers import DoctorSerializer
from core.permissions import IsSuperAdmin, IsHospitalAdminOfSameHospital
from rest_framework.permissions import IsAuthenticated
from rest_framework.viewsets import ModelViewSet
from hospitals.utils import approve_hospital
from django.http import JsonResponse
from .utils import approve_hospital

def approve_hospital_view(request, hospital_id):
    approve_hospital(hospital_id)
    return JsonResponse({'status': 'success', 'message': 'Hospital approved successfully'})

def reject_hospital_view(request, hospital_id):
    hospital = Hospital.objects.get(id=hospital_id)
    hospital.status = Hospital.STATUS_REJECTED
    hospital.save()
    return JsonResponse({'status': 'success', 'message': 'Hospital rejected successfully'})


class HospitalViewSet(ModelViewSet):
    queryset = Hospital.objects.all()
    serializer_class = HospitalRegisterSerializer
    permission_classes = [permissions.IsAuthenticated]

class DepartmentViewSet(viewsets.ModelViewSet):
    queryset = Department.objects.select_related('hospital').all()
    serializer_class = DepartmentSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_permissions(self):
        if self.action in ['create', 'update', 'partial_update', 'destroy']:
            return [permissions.IsAuthenticated(), IsSuperAdmin() | IsHospitalAdminOfSameHospital()]
        return [ permissions.IsAuthenticated()]
    
    def get_queryset(self):
        qs = super().get_queryset()
        hospital_id = self.request.query_params.get('hospital')
        if hospital_id:
            qs = qs.filter(hospital_id=hospital_id)
        return qs


class TreatmentViewSet(viewsets.ModelViewSet):
    queryset = Treatment.objects.select_related('hospital', 'department').all()
    serializer_class = TreatmentSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_permissions(self):
        if self.action in ['create', 'update', 'partial_update', 'destroy']:
            return [permissions.IsAuthenticated(), IsSuperAdmin() | IsHospitalAdminOfSameHospital()]
        return [permissions.IsAuthenticated()]
    
    def get_queryset(self):
        qs = super().get_queryset()
        hospital_id = self.request.query_params.get('hospital')
        department_id = self.request.query_params.get('department')
        if hospital_id:
            qs = qs.filter(hospital_id=hospital_id)
        if department_id:
            qs = qs.filter(department_id=department_id)
        return qs

    
class DoctorViewSet(viewsets.ModelViewSet):
    queryset = Doctor.objects.select_related('hospital', 'department' 'treatment').all()
    serializer_class = DoctorSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_permissions(self):
        if self.action in ['approve', 'reject', 'create', 'update', 'partial_update', 'destroy']:
            return [permissions.IsAuthenticated(), IsSuperAdmin() | IsHospitalAdminOfSameHospital()]
        return [ permissions.IsAuthenticated()]
    
    @decorators.action(detail=True, methods=['post'])
    def approve(self, request, pk=None):
        doctor = self.get_object()
        self.check_object_permissions(request, doctor)
        serializer = self.get_serializer()
        serializer.approve(doctor)
        return response.Response(
            {
                'status': doctor.status, 'is_verified': doctor.is_verified, 'used_id': doctor.id},
            status=status.HTTP_200_OK
        )
    
    @decorators.action(detail=True, methods=['post'])
    def reject(self, request, pk=None):
        Doctor = self.get_object()
        self.check_object_permissions(request, doctor)
        serializer = self.get_serializer()
        serializer.reject(doctor)
        return response.Response(
            {'status': doctor.status, 'is_verified': doctor.is_verified, 'used_id': doctor.id},
            status=status.HTTP_200_OK
        )

