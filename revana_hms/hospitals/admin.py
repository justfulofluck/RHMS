from django.contrib import admin
from django.core.mail import send_mail
from django.contrib.auth import get_user_model
from django.utils.html import format_html
import secrets
from .models import Hospital, Department, Treatment, HospitalAdmin

User = get_user_model()

class DepartmentInline(admin.TabularInline):
    model = Department
    extra = 1

class TreatmentInline(admin.TabularInline):
    model = Treatment
    extra = 1

@admin.register(Hospital)
class HospitalAdminModel(admin.ModelAdmin):
    list_display = ('name', 'email', 'city', 'status', 'country','created_at', 'logo_preview', 'get_admin')
    list_filter = ('status', 'city')
    search_fields = ('name', 'registration_number', 'email')
    actions = ('approve_selected', 'reject_selected')
    inlines = [DepartmentInline, TreatmentInline]
    
    def logo_preview(self, obj):
        if obj.logo:
            return format_html('<img src="{}" style="height:32px;">', obj.logo.url)
        return '-'
    logo_preview.short_description = 'Logo'

    def get_admin(self, obj):
        return obj.admin.user.username if hasattr(obj, 'admin') else '—'
    get_admin.short_description = 'Hospital Admin'

    def approve_selected(self, request, queryset):
        count = 0
        for hospital in queryset.filter(status=Hospital.STATUS_PENDING):
            hospital.status = Hospital.STATUS_APPROVED
            hospital.save()

            user, created = User.objects.get_or_create(
                username=hospital.email,
                defaults={'email': hospital.email, 'is_staff': True, 'is_superuser': False}
            )
            password = secrets.token_urlsafe(10)
            user.set_password(password)
            user.save()

            HospitalAdmin.objects.get_or_create(user=user, hospital=hospital)

            send_mail(
                subject='Hospital Approved - Admin Credentials',
                message=(
                    f'Dear {hospital.name},\n\n'
                    f'Your hospital has been approved.\n\n'
                    f'Login: /admin/\n'
                    f'Username: {hospital.email}\n'
                    f'Password: {password}\n\n'
                    f'Please change your password after first login.'
                ),
                from_email=None,
                recipient_list=[hospital.email],
            )
            count += 1
        self.message_user(request, f'Approved {count} hospital(s) and sent credentials.')
    approve_selected.short_description = 'Approve selected hospitals (create admin + email)'

    def reject_selected(self, request, queryset):
        updated = queryset.exclude(status=Hospital.STATUS_REJECTED).update(status=Hospital.STATUS_REJECTED)
        self.message_user(request, f'Rejected {updated} hospital(s).')
    reject_selected.short_description = 'Reject selected hospitals'

@admin.register(HospitalAdmin)
class HospitalAdminLink(admin.ModelAdmin):
    list_display = ('user', 'get_hospital')
    search_fields = ('user__username', 'hospital__name')

    def get_hospital(self, obj):
        return obj.hospital.name
    get_hospital.short_description = 'Hospital'
