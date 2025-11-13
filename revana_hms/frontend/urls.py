# revana_hms/frontend/urls.py
from django.urls import path
from .views import hospital_register_page,register_hospital_ajax, login_view, hospital_admin_dashboard
from . import views

urlpatterns = [
    path('doctor/dashboard/', views.doctor_dashboard, name='doctor_dashboard'),
    path('hospital/dashboard/', hospital_admin_dashboard, name='hospital_admin_dashboard'),
    path('register-hospital/', hospital_register_page, name='hospital_register_page'),
    path('api/register-hospital/', register_hospital_ajax, name='register_hospital_ajax'),
    path('register-doctor/', views.register_doctor, name='register_doctor'),
    path('login/', login_view, name='login'),
]
