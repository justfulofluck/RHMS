from django.urls import path, include
from rest_framework.routers import DefaultRouter
from appointments.views import AppointmentViewSet, DoctorAvailabilityViewSet, MyAppointmentsViewSet, get_available_slots
from appointments.widget_views import (
    get_cities, get_departments, get_hospitals, get_doctors, get_slots, book_appointment_widget
)


router = DefaultRouter()
router.register(r'appointments', AppointmentViewSet)
router.register(r'availability', DoctorAvailabilityViewSet)
router.register(r'my-appointments', MyAppointmentsViewSet, basename='my-appointments')

urlpatterns = [
    path('', include(router.urls)),
    path('slots/', get_available_slots, name='get_available_slots'),
    
    # Widget APIs
    path('widget/cities/', get_cities, name='widget_cities'),
    path('widget/departments/', get_departments, name='widget_departments'),
    path('widget/hospitals/', get_hospitals, name='widget_hospitals'),
    path('widget/doctors/', get_doctors, name='widget_doctors'),
    path('widget/slots/', get_slots, name='widget_slots'),
    path('widget/book/', book_appointment_widget, name='widget_book'),
]