from django.contrib import admin
from django.utils.html import format_html
from .models import AuditLog
from core.admin import admin_site


@admin.register(AuditLog, site=admin_site)
class AuditLogAdmin(admin.ModelAdmin):
    list_display = (
        "tarih_saat",
        "islem_rozeti",
        "kayit_turu",
        "object_repr",
        "user",
        "birim_adi",
        "ip_address",
    )

    list_filter = ("action", "model", "birim_adi", "created_at")
    search_fields = (
        "object_id",
        "object_repr",
        "user__username",
        "user__email",
        "birim_adi",
        "ip_address",
    )

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

    list_per_page = 25
    ordering = ("-created_at",)
    list_select_related = ("user",)

    def tarih_saat(self, obj):
        return obj.created_at.strftime("%d.%m.%Y %H:%M")
    tarih_saat.short_description = "Tarih / Saat"

    def islem_rozeti(self, obj):
        renkler = {
            "create": "#198754",
            "update": "#0d6efd",
            "delete": "#dc3545",
        }
        etiketler = {
            "create": "Oluşturma",
            "update": "Güncelleme",
            "delete": "Silme",
        }

        renk = renkler.get(obj.action, "#6c757d")
        etiket = etiketler.get(obj.action, obj.action)

        return format_html(
            '<span style="padding:4px 10px; border-radius:999px; color:white; background:{}; font-weight:600;">{}</span>',
            renk,
            etiket,
        )
    islem_rozeti.short_description = "İşlem"

    def kayit_turu(self, obj):
        harita = {
            "Demirbas": "Demirbaş",
            "Personel": "Personel",
            "Birim": "Birim",
            "ZimmetKaydi": "Zimmet Kaydı",
            "AuditLog": "Denetim Kaydı",
            "User": "Kullanıcı",
            "Group": "Grup",
            "KullaniciBirim": "Kullanıcı Birim Eşleştirmesi",
        }
        return harita.get(obj.model, obj.model)
    kayit_turu.short_description = "Kayıt Türü"

    def has_add_permission(self, request):
        return False

    def has_change_permission(self, request, obj=None):
        return False

    def has_delete_permission(self, request, obj=None):
        return False