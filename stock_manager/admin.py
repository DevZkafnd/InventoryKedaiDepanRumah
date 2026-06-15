from django.contrib import admin
from django.apps import AppConfig
from .models import Admin

admin.site.site_header = "Administrasi Kedai Depan Rumah"
admin.site.site_title = "Inventory Kedai Depan Rumah"
admin.site.index_title = "Panel Administrasi"

class AdminAdmin(admin.ModelAdmin):
    exclude = ("edit_lock",)


admin.site.register(Admin, AdminAdmin)
