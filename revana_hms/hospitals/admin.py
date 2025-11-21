from django.contrib import admin
from django.utils.html import format_html
from .models import Hospital, Department, Treatment, HospitalAdmin
from .utils import approve_hospital_and_notify
from django.contrib.auth import get_user_model

User = get_user_model()


class DepartmentInline(admin.TabularInline):
    model = Department
    extra = 1


class TreatmentInline(admin.TabularInline):
    model = Treatment
    extra = 1


@admin.register(Hospital)
class HospitalAdminModel(admin.ModelAdmin):
    list_display = ('name', 'email', 'city', 'status', 'country', 'created_at', 'logo_preview', 'get_admin')
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
        hospital_admin = HospitalAdmin.objects.filter(hospital=obj).first()
        if hospital_admin and hospital_admin.user:
            return getattr(hospital_admin.user, 'email', getattr(hospital_admin.user, 'username', '—'))
        return '—'
    get_admin.short_description = 'Hospital Admin'

    def approve_selected(self, request, queryset):
        count = 0
        for hospital in queryset.filter(status=Hospital.STATUS_PENDING):
            hospital.status = Hospital.STATUS_APPROVED
            hospital.save()

            hospital_admin = HospitalAdmin.objects.filter(hospital=hospital).first()

            # Create HospitalAdmin if missing
            if not hospital_admin:
                user = User.objects.filter(email=hospital.email).first()
                if user:
                    hospital_admin = HospitalAdmin.objects.create(hospital=hospital, user=user)
                    print(f"🔗 Linked hospital to user: {user.email}")
                else:
                    print(f"⚠️ No user found with email {hospital.email}")

            # Assign role if user exists
            if hospital_admin and hospital_admin.user and hospital_admin.user.role != 'hospital_admin':
                hospital_admin.user.role = 'hospital_admin'
                hospital_admin.user.save()
                print(f"✅ Role assigned: {hospital_admin.user.email}")

            print("📤 Bulk approval: sending email to", hospital.email)
            approve_hospital_and_notify(hospital)
            count += 1

        self.message_user(request, f'✅ Approved {count} hospital(s) and sent credentials.')
    approve_selected.short_description = 'Approve selected hospitals (create admin + email)'

    def reject_selected(self, request, queryset):
        updated = queryset.exclude(status=Hospital.STATUS_REJECTED).update(status=Hospital.STATUS_REJECTED)
        self.message_user(request, f'❌ Rejected {updated} hospital(s).')
    reject_selected.short_description = 'Reject selected hospitals'

    def save_model(self, request, obj, form, change):
        if change and obj.status == Hospital.STATUS_APPROVED:
            hospital_admin = HospitalAdmin.objects.filter(hospital=obj).first()

            # Create HospitalAdmin if missing
            if not hospital_admin:
                user = User.objects.filter(email=obj.email).first()
                if user:
                    hospital_admin = HospitalAdmin.objects.create(hospital=obj, user=user)
                    print(f"🔗 Linked hospital to user: {user.email}")
                else:
                    print(f"⚠️ No user found with email {obj.email}")

            # Assign role if user exists
            if hospital_admin and hospital_admin.user and hospital_admin.user.role != 'hospital_admin':
                hospital_admin.user.role = 'hospital_admin'
                hospital_admin.user.save()
                print(f"✅ Role assigned: {hospital_admin.user.email}")

            print("📤 Manual approval: sending email to", obj.email)
            approve_hospital_and_notify(obj)

        super().save_model(request, obj, form, change)


@admin.register(HospitalAdmin)
class HospitalAdminLink(admin.ModelAdmin):
    list_display = ('user_display', 'get_hospital')
    search_fields = ('user__email', 'user__username', 'hospital__name')

    def user_display(self, obj):
        return getattr(obj.user, 'email', getattr(obj.user, 'username', '—'))
    user_display.short_description = 'User'

    def get_hospital(self, obj):
        return obj.hospital.name
    get_hospital.short_description = 'Hospital'
