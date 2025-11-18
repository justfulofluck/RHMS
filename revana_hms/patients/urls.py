from django.urls import path
from . import views

urlpatterns = [
    path('', views.patient_register_page, name='patient_register_page'),
    path('register/', views.register_patient, name='register_patient'),

    # Login
    path('login-page/', views.login_page, name='login_page'),
    path('login/', views.login_user, name='login_user'),

    # Dashboard
    path('dashboard/', views.patient_dashboard, name='patient_dashboard'),

    # Edit Profile
    path('patient/edit-profile/', views.patient_edit_profile, name='patient_edit_profile'),

]
