from django.urls import path
from .views import (
    MobileAdvertisementPublicListAPI,
    MobileAdvertisementAdminListAPI,
    MobileAdvertisementCreateAPI,
    MobileAdvertisementDetailAPI,
)

urlpatterns = [
    path(
        "mobile/",
        MobileAdvertisementPublicListAPI.as_view(),
        name="mobile-advertisements",
    ),
    path(
        "admin/advertisements/",
        MobileAdvertisementAdminListAPI.as_view(),
        name="admin-advertisements-list",
    ),
    path(
        "admin/advertisements/create/",
        MobileAdvertisementCreateAPI.as_view(),
        name="admin-advertisements-create",
    ),
    path(
        "admin/advertisements/<int:pk>/",
        MobileAdvertisementDetailAPI.as_view(),
        name="admin-advertisements-detail",
    ),
]
