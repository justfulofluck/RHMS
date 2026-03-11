from django.db import models
from django.utils import timezone
from rest_framework import status, permissions
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.generics import (
    ListAPIView,
    RetrieveAPIView,
    CreateAPIView,
    UpdateAPIView,
    DestroyAPIView,
)
from .models import MobileAdvertisement
from .serializers import (
    MobileAdvertisementSerializer,
    MobileAdvertisementListSerializer,
)


class IsSuperAdmin(permissions.BasePermission):
    def has_permission(self, request, view):
        return (
            request.user and request.user.is_authenticated and request.user.is_superuser
        )


class MobileAdvertisementPublicListAPI(ListAPIView):
    permission_classes = [permissions.AllowAny]
    serializer_class = MobileAdvertisementListSerializer

    def get_queryset(self):
        now = timezone.now()
        return (
            MobileAdvertisement.objects.filter(
                is_active=True,
            )
            .filter(models.Q(start_date__isnull=True) | models.Q(start_date__lte=now))
            .filter(models.Q(end_date__isnull=True) | models.Q(end_date__gte=now))
            .order_by("display_order", "-created_at")
        )


class MobileAdvertisementAdminListAPI(ListAPIView):
    permission_classes = [IsSuperAdmin]
    serializer_class = MobileAdvertisementSerializer

    def get_queryset(self):
        return MobileAdvertisement.objects.all().order_by("-created_at")


class MobileAdvertisementCreateAPI(CreateAPIView):
    permission_classes = [IsSuperAdmin]
    serializer_class = MobileAdvertisementSerializer


class MobileAdvertisementDetailAPI(RetrieveAPIView, UpdateAPIView, DestroyAPIView):
    permission_classes = [IsSuperAdmin]
    serializer_class = MobileAdvertisementSerializer

    def get_queryset(self):
        return MobileAdvertisement.objects.all()

    def delete(self, request, *args, **kwargs):
        return self.destroy(request, *args, **kwargs)

    def put(self, request, *args, **kwargs):
        return self.update(request, *args, **kwargs)

    def patch(self, request, *args, **kwargs):
        return self.partial_update(request, *args, **kwargs)
