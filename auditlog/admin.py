# auditlog/admin.py
from django.contrib import admin
from .models import AuditLog
from core.admin import admin_site


@admin.register(AuditLog, site=admin_site)
class AuditLogAdmin(admin.ModelAdmin):
    list_display = (
        "created_at",
        "action",
        "model",
        "object_id",
        "object_repr",
        "user",
        "birim_adi",
        "ip_address",
    )
    list_filter = ("action", "model", "birim_adi", "created_at")
    search_fields = ("object_id", "object_repr", "user__username", "user__email", "birim_adi", "ip_address")
    readonly_fields = (
        "created_at",
        "action",
        "model",
        "object_id",
        "object_repr",
        "user",
        "birim_adi",
        "ip_address",
        "extra",
    )

    def has_add_permission(self, request):
        return False  # log sadece sistem tarafından yazılır

    def has_change_permission(self, request, obj=None):
        return False  # log değiştirilemez

    def has_delete_permission(self, request, obj=None):
        return False  # log silinmesin (kurumsal)