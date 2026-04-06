from django.conf import settings
from django.db import models


class AuditLog(models.Model):
    ACTION_CREATE = "create"
    ACTION_UPDATE = "update"
    ACTION_DELETE = "delete"

    ACTION_CHOICES = (
        (ACTION_CREATE, "Oluşturma"),
        (ACTION_UPDATE, "Güncelleme"),
        (ACTION_DELETE, "Silme"),
    )

    created_at = models.DateTimeField("Tarih", auto_now_add=True)

    action = models.CharField("İşlem", max_length=10, choices=ACTION_CHOICES)
    model = models.CharField("Kayıt Türü", max_length=100)
    object_id = models.CharField("Kayıt ID", max_length=50)
    object_repr = models.CharField("Kayıt", max_length=255)

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="audit_logs",
        verbose_name="Kullanıcı",
    )

    birim_adi = models.CharField("Birim", max_length=150, blank=True, default="")
    ip_address = models.GenericIPAddressField("IP Adresi", null=True, blank=True)

    extra = models.JSONField("Ek Veri", blank=True, default=dict)

    class Meta:
        verbose_name = "Denetim Kaydı"
        verbose_name_plural = "Denetim Kayıtları"
        ordering = ("-created_at",)

    def __str__(self):
        return f"[{self.created_at:%d.%m.%Y %H:%M}] {self.get_action_display()} {self.model}#{self.object_id}"