from django.contrib import admin
from .models import MobileAdvertisement


@admin.register(MobileAdvertisement)
class MobileAdvertisementAdmin(admin.ModelAdmin):
    list_display = [
        "id",
        "title",
        "is_active",
        "display_order",
        "start_date",
        "end_date",
        "created_at",
    ]
    list_filter = ["is_active", "created_at"]
    search_fields = ["title", "description"]
    ordering = ["display_order", "-created_at"]
    readonly_fields = ["created_at", "updated_at"]

    fieldsets = (
        (
            "Banner Information",
            {"fields": ("banner_image", "title", "description", "link_url")},
        ),
        ("Settings", {"fields": ("is_active", "display_order")}),
        ("Scheduling", {"fields": ("start_date", "end_date")}),
        (
            "Timestamps",
            {"fields": ("created_at", "updated_at"), "classes": ("collapse",)},
        ),
    )
