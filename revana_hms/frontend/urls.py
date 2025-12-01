# revana_hms/frontend/urls.py
from django.urls import path
from accounts.views import superadmin_login_ajax
from .views import (
    hospital_register_page,
    register_hospital_ajax,
    reset_password_confirm_page,
    request_password_reset_page,
    hospital_login_view,
    approve_hospital,
    homepage,
    appointment_widget,
)
from doctors.views import hospital_admin_dashboard
from . import views

urlpatterns = [
    path('', homepage, name='homepage'),
    path('hospital/dashboard/', hospital_admin_dashboard, name='hospital_admin_dashboard'),
    path('register-hospital/', hospital_register_page, name='hospital_register_page'),
    path('api/register-hospital/', register_hospital_ajax, name='register_hospital_ajax'),
    path('hospital/login/', hospital_login_view, name='hospital_login'),
    path('reset-password-confirm/', reset_password_confirm_page, name='reset_password_confirm_page'),
    path('request-password-reset/', request_password_reset_page, name='request_password_reset_page'),
    path('hospital/edit/', views.edit_hospital_admin, name='edit_hospital_info'),
    path('superadmin/hospital/approve/<int:hospital_id>/', views.approve_hospital, name='approve_hospital'),
    path('book-appointment/', appointment_widget, name='appointment_widget'),
    
]
