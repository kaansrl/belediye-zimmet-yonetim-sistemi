from django.contrib import admin
from django.utils.html import format_html
from django.urls import reverse

from .models import ZimmetKaydi
from core.admin import admin_site


def is_admin(user):
    return user.is_superuser or user.groups.filter(name="Admin").exists()


def get_user_birim(user):
    kb = getattr(user, "birim_bilgisi", None)
    return kb.birim if kb else None


@admin.register(ZimmetKaydi, site=admin_site)
class ZimmetKaydiAdmin(admin.ModelAdmin):

    list_display = (
        "demirbas",
        "personel",
        "durum",
        "verilme_tarihi",
        "iade_tarihi",
        "pdf_indir",   # 👈 yeni sütun
    )

    list_filter = ("durum",)

    search_fields = (
        "demirbas__kod",
        "demirbas__ad",
        "personel__ad_soyad",
        "personel__sicil_no",
    )

    # PDF linki
    def pdf_indir(self, obj):
        url = reverse("zimmet_pdf", args=[obj.id])
        return format_html(
            '<a class="button" href="{}" target="_blank">PDF indir</a>',
            url
        )

    pdf_indir.short_description = "PDF"

    def get_queryset(self, request):
        qs = super().get_queryset(request)

        if is_admin(request.user):
            return qs

        birim = get_user_birim(request.user)

        if birim:
            return qs.filter(demirbas__birim=birim)

        return qs.none()

    # Birim Yetkilisi view-only, Admin CRUD
    def has_add_permission(self, request):
        return is_admin(request.user)

    def has_change_permission(self, request, obj=None):
        return is_admin(request.user)

    def has_delete_permission(self, request, obj=None):
        return is_admin(request.user)