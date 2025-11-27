from django.urls import path
from .admin_views import list_hospital_admins, list_doctors, delete_user

urlpatterns = [
    path('hospital_admins/', list_hospital_admins, name='list_hospital_admins'),
    path('doctors/', list_doctors, name='list_doctors'),
    path('users/<int:user_id>/', delete_user, name='delete_user'),
]
