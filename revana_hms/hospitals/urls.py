from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import HospitalViewSet
from .views import approve_hospital_view, reject_hospital_view
from . import views
from django.urls import path
from .views import approve_hospital_view, reject_hospital_view

urlpatterns = [
    path('superadmin/hospital/approve/<int:hospital_id>/', approve_hospital_view, name='approve_hospital'),
    path('superadmin/hospital/reject/<int:hospital_id>/', reject_hospital_view, name='reject_hospital'),
]


app_name = 'hospitals'
router = DefaultRouter()
router.register(r'hospitals', HospitalViewSet, basename='hospital')

urlpatterns = [
    path('api/', include(router.urls)),
    path('superadmin/hospital/approve/<int:hospital_id>/', approve_hospital_view, name='approve_hospital'),
    path('superadmin/hospital/reject/<int:hospital_id>/', reject_hospital_view, name='reject_hospital'),
    path('register/', views.RegisterView.as_view(), name='register')
]
