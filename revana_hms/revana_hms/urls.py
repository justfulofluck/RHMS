# """
# URL configuration for revana_hms project.

# The `urlpatterns` list routes URLs to views. For more information please see:
#     https://docs.djangoproject.com/en/5.2/topics/http/urls/
# Examples:
# Function views
#     1. Add an import:  from my_app import views
#     2. Add a URL to urlpatterns:  path('', views.home, name='home')
# Class-based views
#     1. Add an import:  from other_app.views import Home
#     2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
# Including another URLconf
#     1. Import the include() function: from django.urls import include, path
#     2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
# """

from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

# ViewSets with aliasing to avoid conflicts
from doctors.views import (
    DoctorViewSet,
    DoctorAvailabilityViewSet as DoctorAvailabilityFromDoctors,
    DoctorAvailabilityViewSet as DoctorAvailabilityFromDoctors,
    PublicAvailabilityViewSet,
    doctor_login_view
)
from appointments.views import (
    AppointmentViewSet,
    DoctorAvailabilityViewSet as DoctorAvailabilityFromAppointments,
    CalendarView,
    MobileBookingView
)
from hospitals.views import DepartmentViewSet, TreatmentViewSet, RegisterView
from core.views import test_auth, universal_search
from accounts.views import logout_view, universal_login_view

# DRF Router setup
router = DefaultRouter()
router.register(r'doctors', DoctorViewSet, basename='doctor')
router.register(r'availability', DoctorAvailabilityFromDoctors, basename='availability')
router.register(r'public-availability', PublicAvailabilityViewSet, basename='public-availability')
router.register(r'appointments', AppointmentViewSet, basename='appointment')
router.register(r'doctor-availabilities', DoctorAvailabilityFromAppointments, basename='doctor-availability')
router.register(r'departments', DepartmentViewSet, basename='department')
router.register(r'treatments', TreatmentViewSet, basename='treatment')

urlpatterns = [
    path('admin/', admin.site.urls),

    # JWT Auth
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),

    # Core API
    path('api/test-auth/', test_auth),
    path('api/universal-search/', universal_search, name='universal_search'),
    
    # Global Login/Logout (prevents 500 and 404 errors)
    path('login/', universal_login_view, name='login'),
    path('logout/', logout_view, name='logout'),

    # App-specific routes
    path('hospitals/', include('hospitals.urls')),
    path('api/admin/', include('accounts.admin_urls')),
    path('api/accounts/', include('accounts.api_urls')),
    path('api/hospitals/', include('hospitals.api_urls')),
    path('accounts/', include('accounts.urls')),
    path('inbox/notifications/', include('notifications.urls', namespace='notifications')),
    path('api/appointments/', include('appointments.urls')),
    path('appointments/', include('appointments.urls')),

    # DRF router endpoints
    path('api/', include(router.urls)),

    # Other views
    path('register/', RegisterView.as_view(), name='register'),
    path('calendar/', CalendarView.as_view(), name='calendar-view'),
    path('mobile/book/', MobileBookingView.as_view(), name='mobile-booking'),

    # Frontend and doctor modules
    path('', include('frontend.urls')),
    path('patients/', include('patients.urls')),
    path('hospital/doctors/', include('doctors.urls')),

    # Homepage
    path('', include('frontend.urls')),
    path('', include('appointments.urls')),
    path('admin/', admin.site.urls),
]

# Media files
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

