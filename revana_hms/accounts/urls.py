from django.urls import path
from .views import PasswordResetRequestView, PasswordResetConfirmView, export_appointments_csv, superadmin_login_ajax
from django.contrib.auth.views import LogoutView

urlpatterns = [
    path('password-reset/', PasswordResetRequestView.as_view(), name='password_reset'),
    path('password-reset-confirm/', PasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    path('export-appointments/', export_appointments_csv, name='export_appointments'),
    path('logout/', LogoutView.as_view(next_page='superadmin_login'), name='logout'),
    path('superadmin/login/', superadmin_login_ajax, name='superadmin_login'),
]

