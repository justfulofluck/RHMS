from rest_framework import serializers
from .models import MobileAdvertisement


class MobileAdvertisementSerializer(serializers.ModelSerializer):
    is_currently_active = serializers.BooleanField(read_only=True)

    class Meta:
        model = MobileAdvertisement
        fields = [
            "id",
            "banner_image",
            "title",
            "description",
            "link_url",
            "is_active",
            "display_order",
            "start_date",
            "end_date",
            "created_at",
            "updated_at",
            "is_currently_active",
        ]
        read_only_fields = ["id", "created_at", "updated_at"]


class MobileAdvertisementListSerializer(serializers.ModelSerializer):
    image_url = serializers.SerializerMethodField()

    class Meta:
        model = MobileAdvertisement
        fields = [
            "id",
            "image_url",
            "title",
            "description",
            "link_url",
        ]

    def get_image_url(self, obj):
        if obj.banner_image:
            request = self.context.get("request")
            if request:
                return request.build_absolute_uri(obj.banner_image.url)
            return obj.banner_image.url
        return None
