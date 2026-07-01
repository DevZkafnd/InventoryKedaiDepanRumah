from django.contrib import admin
from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group
from django.contrib.sessions.models import Session

from .models import Admin, WasteItem

admin.site.site_header = "Administrasi Kedai Depan Rumah"
admin.site.site_title = "Inventory Kedai Depan Rumah"
admin.site.index_title = "Panel Administrasi"

User = get_user_model()

try:
    admin.site.unregister(User)
except Exception:
    pass

try:
    admin.site.unregister(Group)
except Exception:
    pass

try:
    from axes.models import AccessAttempt

    admin.site.unregister(AccessAttempt)
except Exception:
    pass

try:
    admin.site.unregister(Session)
except Exception:
    pass


@admin.register(Admin)
class AdminConfigAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "edit_lock",
        "allow_uploads",
        "allow_upload_deletions",
        "allow_email_notifications",
        "records_per_page",
    )
    list_editable = (
        "edit_lock",
        "allow_uploads",
        "allow_upload_deletions",
        "allow_email_notifications",
        "records_per_page",
    )
    ordering = ("id",)


@admin.register(WasteItem)
class WasteItemAdmin(admin.ModelAdmin):
    list_display = ("recorded_at", "item", "source", "quantity", "reason", "created_at")
    list_filter = ("source", "recorded_at")
    search_fields = ("item__sku", "item__description", "reason")
