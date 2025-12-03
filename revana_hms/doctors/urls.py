from django.urls import path
from . import views

urlpatterns = [
    path('', views.doctor_register_page, name='doctor_register_page'),
    path('register/', views.register_doctor, name='register_doctor'),
    path('pending/', views.pending_doctors, name='pending_doctors'),
    path('approve/<int:doctor_id>/', views.approve_doctor, name='approve_doctor'),
    path('edit/<int:doctor_id>/', views.edit_doctor, name='edit_doctor'),
    path('login/', views.doctor_login_view, name='doctor_login'),
    path('dashboard/', views.doctor_dashboard, name='doctor_dashboard'),
    path('hospital/dashboard/', views.hospital_admin_dashboard, name='hospital_dashboard'),
    path('approve/<int:doctor_id>/', views.approve_doctor, name='approve_doctor'),
]
