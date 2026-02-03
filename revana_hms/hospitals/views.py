from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from django.views.generic import TemplateView
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from rest_framework import viewsets, permissions ,decorators, response, status
from doctors.models import Doctor
from .models import Department, Treatment, Hospital, HospitalAdmin
from .serializers import DepartmentSerializer, TreatmentSerializer, HospitalRegisterSerializer
from doctors.serializers import DoctorSerializer
from core.permissions import IsSuperAdmin, IsHospitalAdminOfSameHospital
from rest_framework.permissions import IsAuthenticated
from rest_framework.viewsets import ModelViewSet
from accounts.models import DoctorProfile
from django.http import JsonResponse
from hospitals.utils import approve_hospital_and_notify  # Only if actually used in views




class RegisterView(TemplateView):
    template_name = 'register.html' 

def approve_hospital_view(request, hospital_id):
    approve_hospital_and_notify (hospital_id)
    return JsonResponse({'status': 'success', 'message': 'Hospital approved successfully'})

def reject_hospital_view(request, hospital_id):
    hospital = Hospital.objects.get(id=hospital_id)
    hospital.status = Hospital.STATUS_REJECTED
    hospital.save()
    return JsonResponse({'status': 'success', 'message': 'Hospital rejected successfully'})


class HospitalViewSet(ModelViewSet):
    # Only show approved hospitals to non-admin users
    queryset = Hospital.objects.filter(status=Hospital.STATUS_APPROVED)
    serializer_class = HospitalRegisterSerializer
    permission_classes = [permissions.IsAuthenticated]

class DepartmentViewSet(viewsets.ModelViewSet):
    queryset = Department.objects.select_related('hospital').all()
    serializer_class = DepartmentSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def get_permissions(self):
        if self.action in ['create', 'update', 'partial_update', 'destroy']:
            return [permissions.IsAuthenticated(), IsSuperAdmin() | IsHospitalAdminOfSameHospital()]
        return [permissions.IsAuthenticatedOrReadOnly()]
    
    def get_queryset(self):
        qs = super().get_queryset()
        hospital_id = self.request.query_params.get('hospital')
        if hospital_id:
            qs = qs.filter(hospital_id=hospital_id)
        return qs


class TreatmentViewSet(viewsets.ModelViewSet):
    queryset = Treatment.objects.select_related('hospital', 'department').all()
    serializer_class = TreatmentSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    
    def get_permissions(self):
        if self.action in ['create', 'update', 'partial_update', 'destroy']:
            return [permissions.IsAuthenticated(), IsSuperAdmin() | IsHospitalAdminOfSameHospital()]
        return [permissions.IsAuthenticatedOrReadOnly()]
    
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


@login_required
def manage_departments(request):
    try:
        hospital_admin = HospitalAdmin.objects.get(user=request.user)
        hospital = hospital_admin.hospital
    except HospitalAdmin.DoesNotExist:
        messages.error(request, "You are not authorized to view this page.")
        return redirect('homepage')

    if request.method == 'POST':
        if 'create' in request.POST:
            name = request.POST.get('name')
            if name:
                Department.objects.create(hospital=hospital, name=name)
                messages.success(request, 'Department created successfully.')
        elif 'delete' in request.POST:
            department_id = request.POST.get('department_id')
            department = get_object_or_404(Department, id=department_id, hospital=hospital)
            department.delete()
            messages.success(request, 'Department deleted successfully.')
        return redirect('hospitals:manage_departments')

    departments = Department.objects.filter(hospital=hospital)
    return render(request, 'hospitals/manage_departments.html', {'departments': departments, 'hospital': hospital})

@login_required
def manage_treatments(request):
    try:
        hospital_admin = HospitalAdmin.objects.get(user=request.user)
        hospital = hospital_admin.hospital
    except HospitalAdmin.DoesNotExist:
        messages.error(request, "You are not authorized to view this page.")
        return redirect('homepage')

    departments = Department.objects.filter(hospital=hospital)

    if request.method == 'POST':
        if 'create' in request.POST:
            name = request.POST.get('name')
            department_id = request.POST.get('department_id')
            cost = request.POST.get('cost')
            duration = request.POST.get('duration')
            
            if name and department_id:
                department = get_object_or_404(Department, id=department_id, hospital=hospital)
                Treatment.objects.create(
                    hospital=hospital, 
                    department=department, 
                    name=name,
                    # cost=cost, # Add these fields to model if needed
                    # duration=duration
                )
                messages.success(request, 'Treatment created successfully.')
        elif 'delete' in request.POST:
            treatment_id = request.POST.get('treatment_id')
            treatment = get_object_or_404(Treatment, id=treatment_id, hospital=hospital)
            treatment.delete()
            messages.success(request, 'Treatment deleted successfully.')
        return redirect('hospitals:manage_treatments')

    treatments = Treatment.objects.filter(hospital=hospital).select_related('department')
    return render(request, 'hospitals/manage_treatments.html', {'treatments': treatments, 'departments': departments, 'hospital': hospital})

def department_list(request):
    # Only show departments from approved hospitals
    departments = Department.objects.select_related('hospital').filter(
        hospital__status=Hospital.STATUS_APPROVED
    )
    return render(request, 'frontend/departments.html', {'departments': departments})

def department_detail(request, department_id):
    # Only show department if hospital is approved
    department = get_object_or_404(
        Department.objects.select_related('hospital'),
        id=department_id,
        hospital__status=Hospital.STATUS_APPROVED
    )
    treatments = department.treatments.all()
    doctors = department.doctors.all()
    return render(request, 'frontend/department_detail.html', {
        'department': department,
        'treatments': treatments,
        'doctors': doctors
    })

def get_nearby_hospitals(request):
    """
    API for getting nearby hospitals based on lat/lng.
    Currently returns empty list as Hospital model needs lat/lng fields.
    """
    return JsonResponse({'hospitals': []})
