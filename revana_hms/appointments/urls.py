from django.urls import path, include
from rest_framework.routers import DefaultRouter
from appointments.views import (
    AppointmentViewSet, DoctorAvailabilityViewSet, MyAppointmentsViewSet, 
    get_available_slots, cancel_appointment, mobile_booking_view, get_mobile_slots,
    MobileBookingView, call_next_patient, get_queue_status, mobile_doctor_slots # Added
)
from appointments.widget_views import (
    get_cities, get_departments, get_hospitals, get_doctors, get_slots, book_appointment_widget
)


router = DefaultRouter()
router.register(r'appointments', AppointmentViewSet)
router.register(r'availability', DoctorAvailabilityViewSet)
router.register(r'my-appointments', MyAppointmentsViewSet, basename='my-appointments')

urlpatterns = [
    # Queue Management (Doctor Console) - Moved to top to avoid router conflicts
    path('doctor/queue/next/', call_next_patient, name='queue_next'),
    path('doctor/queue/status/', get_queue_status, name='queue_status'),

    path('', include(router.urls)),
    path('slots/', get_available_slots, name='get_available_slots'),
    
    # Widget APIs
    path('widget/cities/', get_cities, name='widget_cities'),
    path('widget/departments/', get_departments, name='widget_departments'),
    path('widget/hospitals/', get_hospitals, name='widget_hospitals'),
    path('widget/doctors/', get_doctors, name='widget_doctors'),
    path('widget/slots/', get_slots, name='widget_slots'),
    path('widget/book/', book_appointment_widget, name='widget_book'),
    
    # Actions
    path('cancel/<int:appointment_id>/', cancel_appointment, name='cancel_appointment'),
    
    # 📱 Mobile Booking
    path('book/mobile/<int:doctor_id>/', mobile_booking_view, name='mobile_booking'),
    path('api/mobile-slots/<int:doctor_id>/', get_mobile_slots, name='get_mobile_slots'),
    path('api/mobile-doctor-slots/<int:doctor_id>/', mobile_doctor_slots, name='mobile_doctor_slots'),
    path('api/mobile-book/', MobileBookingView.as_view(), name='mobile_book_api'),
    
]