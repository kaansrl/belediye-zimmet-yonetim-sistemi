# auditlog/models.py
from django.conf import settings
from django.db import models


class AuditLog(models.Model):
    ACTION_CREATE = "create"
    ACTION_UPDATE = "update"
    ACTION_DELETE = "delete"

    ACTION_CHOICES = (
        (ACTION_CREATE, "Create"),
        (ACTION_UPDATE, "Update"),
        (ACTION_DELETE, "Delete"),
    )

    created_at = models.DateTimeField(auto_now_add=True)

    action = models.CharField(max_length=10, choices=ACTION_CHOICES)
    model = models.CharField(max_length=100)          # örn: "Demirbas"
    object_id = models.CharField(max_length=50)       # pk, string tutuyoruz (esnek)
    object_repr = models.CharField(max_length=255)    # örn: "DB-2026-0003 - HP..."

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="audit_logs",
    )

    birim_adi = models.CharField(max_length=150, blank=True, default="")
    ip_address = models.GenericIPAddressField(null=True, blank=True)

    extra = models.JSONField(blank=True, default=dict)

    class Meta:
        ordering = ("-created_at",)

    def __str__(self):
        return f"[{self.created_at:%Y-%m-%d %H:%M}] {self.action.upper()} {self.model}#{self.object_id}"