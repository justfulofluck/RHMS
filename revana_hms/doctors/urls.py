from django.urls import path
from . import views
from .monthly_views import create_monthly_availability, doctor_availability_list, delete_availability, get_booked_dates

urlpatterns = [
    path('', views.doctor_register_page, name='doctor_register_page'),
    path('register/', views.register_doctor, name='register_doctor'),
    path('pending/', views.pending_doctors, name='pending_doctors'),
    path('approve/<int:doctor_id>/', views.approve_doctor, name='approve_doctor'),
    path('edit/<int:doctor_id>/', views.edit_doctor, name='edit_doctor'),
    path('login/', views.doctor_login_view, name='doctor_login'),
    path('profile/edit/', views.edit_my_profile, name='doctor_profile_edit'),
    path('dashboard/', views.doctor_dashboard, name='doctor_dashboard'),
    path('hospital/dashboard/', views.hospital_admin_dashboard, name='hospital_dashboard'),
    
    # Availability management
    path('availability/monthly/', create_monthly_availability, name='monthly_availability'),
    path('availability/', doctor_availability_list, name='doctor_availability_list'),
    path('availability/delete/<int:availability_id>/', delete_availability, name='delete_availability'),
    path('availability/api/booked-dates/', get_booked_dates, name='get_booked_dates'),
    
    # Appointment Actions
    path('appointment/update-status/<int:appointment_id>/', views.update_appointment_status, name='update_appointment_status'),
    path('my-patients/', views.my_patients_view, name='my_patients'),
]
