from django.db import models
from django.utils import timezone


def advertisement_image_path(instance, filename):
    ext = filename.split(".")[-1]
    return f"advertisements/mobile/{instance.id}.{ext}"


class MobileAdvertisement(models.Model):
    banner_image = models.ImageField(
        upload_to=advertisement_image_path, blank=True, null=True
    )
    title = models.CharField(max_length=200, blank=True)
    description = models.TextField(blank=True)
    link_url = models.URLField(blank=True, null=True)
    is_active = models.BooleanField(default=True)
    display_order = models.PositiveIntegerField(default=0)
    start_date = models.DateTimeField(null=True, blank=True)
    end_date = models.DateTimeField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "mobile_advertisements"
        ordering = ["display_order", "-created_at"]

    def __str__(self):
        return self.title or f"Advertisement #{self.id}"

    @property
    def is_currently_active(self):
        now = timezone.now()
        if not self.is_active:
            return False
        if self.start_date and self.start_date > now:
            return False
        if self.end_date and self.end_date < now:
            return False
        return True
