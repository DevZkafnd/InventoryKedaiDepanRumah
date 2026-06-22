from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.views.generic import RedirectView
from stock_manager.views import landing, logout_view

urlpatterns = []

if not getattr(settings, "ALLOW_PW_CHANGE", True):
    urlpatterns += [
        path("accounts/password_change/", RedirectView.as_view(url="/")),
        path("admin/password_change/", RedirectView.as_view(url="/admin/")),
        path("admin/password_change/done/", RedirectView.as_view(url="/admin/")),
    ]

urlpatterns += [
    path("", landing, name="landing"),  # Landing page sebagai homepage
    path("", include("stock_manager.urls")),
    path("admin/", admin.site.urls),
    path("api/", include("stock_manager.urls")),
    path("api/ai/", include("ai_service.urls")),
    path("accounts/logout/", logout_view, name="logout"),
    path("accounts/", include("django.contrib.auth.urls")),
    path("api/auth/", include("rest_framework.urls")),
]
