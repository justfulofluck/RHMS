from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import HospitalViewSet, approve_hospital_view, reject_hospital_view, get_nearby_hospitals
from . import views

app_name = 'hospitals'

router = DefaultRouter()
router.register(r'hospitals', HospitalViewSet, basename='hospital')

urlpatterns = [
    path('api/', include(router.urls)),
    path('superadmin/hospital/approve/<int:hospital_id>/', approve_hospital_view, name='approve_hospital'),
    path('superadmin/hospital/reject/<int:hospital_id>/', reject_hospital_view, name='reject_hospital'),
    path('nearby/', get_nearby_hospitals, name='nearby_hospitals'),
    path('register/', views.RegisterView.as_view(), name='register'),
    
    # Management URLs
    path('manage/departments/', views.manage_departments, name='manage_departments'),
    path('manage/treatments/', views.manage_treatments, name='manage_treatments'),
    
    # Public URLs
    path('departments/', views.department_list, name='department_list'),
    path('departments/<int:department_id>/', views.department_detail, name='department_detail'),
]
