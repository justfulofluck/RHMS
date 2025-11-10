"""
URL configuration for revana_hms project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from hospitals import api_views
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)
from rest_framework.routers import DefaultRouter
from doctors.views import DoctorViewSet, DoctorAvailabilityViewSet, PublicAvailabilityViewSet
from appointments.views import AppointmentViewSet, DoctorAvailabilityViewSet, CalendarView, MobileBookingView
from hospitals.views import DepartmentViewSet, TreatmentViewSet
from core.views import test_auth


router = DefaultRouter()
router.register(r'doctors', DoctorViewSet, basename='doctor')
router.register(r'availability', DoctorAvailabilityViewSet, basename='availability')
router.register(r'public-availability', PublicAvailabilityViewSet, basename='public-availability')
router.register(r'appointments', AppointmentViewSet, basename='appointment')
router.register(r'doctor-availabilities', DoctorAvailabilityViewSet, basename='doctor-availability')
router.register(r'departments', DepartmentViewSet, basename='department')
router.register(r'treatments', TreatmentViewSet, basename='treatment')

urlpatterns = [
    path('api/test-auth/', test_auth),
    path('admin/', admin.site.urls),
    path('api/', include('hospitals.api_urls')),
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('api/accounts/', include('accounts.urls')),
    path('api/', include(router.urls)),
    path('api/appointments/', include('appointments.urls')),
    path('calendar/', CalendarView.as_view(), name='calendar-view'),
    path('mobile/book/', MobileBookingView.as_view(), name='mobile-booking'),
    path('', include('frontend.urls')),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
