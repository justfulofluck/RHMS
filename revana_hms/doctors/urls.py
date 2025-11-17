from django.urls import path
from . import views

urlpatterns = [
    path('', views.doctor_register_page, name='doctor_register_page'),
    path('register/', views.register_doctor, name='register_doctor'),
]
