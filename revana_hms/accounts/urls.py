from django.urls import path
from .views import (
    PasswordResetRequestView, 
    PasswordResetConfirmView, 
    export_appointments_csv, 
    superadmin_login_ajax,
    superadmin_dashboard,
    manage_registrations,
    logout_view,
    delete_user,
    superadmin_search
)
from django.contrib.auth.views import LogoutView

urlpatterns = [
    path('request-password-reset/', PasswordResetRequestView.as_view(), name='request-password-reset'),
    path('reset-password-confirm/', PasswordResetConfirmView.as_view(), name='reset-password-confirm'),
    path('logout/', logout_view, name='logout'),
    path('delete-user/<int:user_id>/', delete_user, name='delete_user'),
    path('export-appointments/', export_appointments_csv, name='export_appointments'),
    path('superadmin/login/', superadmin_login_ajax, name='superadmin_login'),
    path('superadmin/dashboard/', superadmin_dashboard, name='superadmin_dashboard'),
    path('superadmin/manage-registrations/', manage_registrations, name='manage_registrations'),
    path('superadmin/search/', superadmin_search, name='superadmin_search'),
]
