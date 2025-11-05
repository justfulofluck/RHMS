from django.urls import path, include
from .views import register_hospital_view, thank_you_view
from rest_framework.routers import DefaultRouter
from .views import HospitalViewSet



app_name = 'hospitals'
router = DefaultRouter()
router.register(r'hospitals', HospitalViewSet, basename='hospital')

urlpatterns = [
    path('register/', register_hospital_view, name='register'),
    path('thank-you/', thank_you_view, name='thank_you'),
    path('api/', include(router.urls)),
]
