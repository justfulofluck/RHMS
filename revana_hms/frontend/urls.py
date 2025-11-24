# revana_hms/frontend/urls.py
from django.urls import path
from accounts.views import superadmin_login_ajax, superadmin_dashboard
from .views import (
    hospital_register_page,
    register_hospital_ajax,
    hospital_admin_dashboard,
    reset_password_confirm_page,
    request_password_reset_page,
    doctor_login_view,
    hospital_login_view,
)
from . import views

urlpatterns = [
    path('doctor/dashboard/', views.doctor_dashboard, name='doctor_dashboard'),
    path('doctor/register/', views.doctor_register_page, name='doctor_register_page'),
    path('hospital/dashboard/', views.hospital_admin_dashboard, name='hospital_admin_dashboard'),
    path('register-hospital/', hospital_register_page, name='hospital_register_page'),
    path('api/register-hospital/', register_hospital_ajax, name='register_hospital_ajax'),
    path('register-doctor/', views.register_doctor_ajax, name='register_doctor'),
    path('doctor/login/', doctor_login_view, name='doctor_login'),
    path('hospital/login/', hospital_login_view, name='hospital_login'),
    path('reset-password-confirm/', reset_password_confirm_page, name='reset_password_confirm_page'),
    path('request-password-reset/', request_password_reset_page, name='request_password_reset_page'),
    path('superadmin/login/', superadmin_login_ajax, name='superadmin_login_ajax'),
    path('superadmin/dashboard/', superadmin_dashboard, name='superadmin_dashboard'),

]
