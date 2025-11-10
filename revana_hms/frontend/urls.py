# revana_hms/frontend/urls.py
from django.urls import path
from .views import register_hospital, login_view
from . import views

urlpatterns = [
    path('hospital-admin/dashboard/', views.hospital_admin_dashboard, name='hospital_admin_dashboard'),
    path('doctor/dashboard/', views.doctor_dashboard, name='doctor_dashboard'),
    path('register-hospital/', register_hospital, name='register'),
    #path('register-hospital/', views.register_hospital, name='register_hospital'),
    #path('register-hospital-admin/', views.register_hospital_admin, name='register_hospital'),
    path('register-doctor/', views.register_doctor, name='register_doctor'),
    #path('login/', views.user_login, name='login'),
    path('login/', login_view, name='login'),
]
