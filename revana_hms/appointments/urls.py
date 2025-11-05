from django.urls import path, include
from rest_framework.routers import DefaultRouter
from appointments.views import AppointmentViewSet, DoctorAvailabilityViewSet, MyAppointmentsViewSet

router = DefaultRouter()
router.register(r'appointments', AppointmentViewSet)
router.register(r'availability', DoctorAvailabilityViewSet)
router.register(r'my-appointments', MyAppointmentsViewSet, basename='my-appointments')

urlpatterns = [
    path('', include(router.urls)),
]