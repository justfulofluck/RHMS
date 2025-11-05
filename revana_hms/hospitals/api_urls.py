from django.urls import path
from .api_views import HospitalRegisterAPI, HospitalListAPI, ApproveHospitalAPI

urlpatterns = [
    path('hospitals/register/', HospitalRegisterAPI.as_view(), name='api_hospital_register'),
    path('hospitals/', HospitalListAPI.as_view(), name='api_hospitals_list'),
    path('admin/hospitals/<int:hospital_id>/approve/', ApproveHospitalAPI.as_view(), name='api_approve_hospital'),
]
