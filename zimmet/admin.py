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
        "durum_rozeti",
        "verilme_tarihi_formatli",
        "iade_tarihi_formatli",
        "pdf_indir",
    )

    list_filter = ("durum",)
    search_fields = (
        "demirbas__kod",
        "demirbas__ad",
        "personel__ad_soyad",
        "personel__sicil_no",
    )

    list_per_page = 20
    ordering = ("-verilme_tarihi",)
    list_select_related = ("demirbas", "personel")

    # 🔵 DURUM ROZETİ
    def durum_rozeti(self, obj):
        renkler = {
            "aktif": "#0d6efd",   # mavi
            "iade": "#198754",    # yeşil
        }
        etiketler = {
            "aktif": "Aktif",
            "iade": "İade Edildi",
        }

        renk = renkler.get(obj.durum, "#6c757d")
        etiket = etiketler.get(obj.durum, obj.durum)

        return format_html(
            '<span style="padding:4px 10px; border-radius:999px; color:white; background:{}; font-weight:600;">{}</span>',
            renk,
            etiket,
        )

    durum_rozeti.short_description = "Durum"

    # 📅 TARİH FORMATLAMA
    def verilme_tarihi_formatli(self, obj):
        return obj.verilme_tarihi.strftime("%d.%m.%Y")
    verilme_tarihi_formatli.short_description = "Verilme Tarihi"

    def iade_tarihi_formatli(self, obj):
        if obj.iade_tarihi:
            return obj.iade_tarihi.strftime("%d.%m.%Y")
        return "-"
    iade_tarihi_formatli.short_description = "İade Tarihi"

    # 📄 PDF BUTONU
    def pdf_indir(self, obj):
        url = reverse("zimmet_pdf", args=[obj.id])
        return format_html(
            '<a class="button" href="{}" target="_blank">PDF</a>',
            url
        )
    pdf_indir.short_description = "Belge"

    # 🔒 QUERYSET KONTROLÜ
    def get_queryset(self, request):
        qs = super().get_queryset(request)

        if is_admin(request.user):
            return qs

        birim = get_user_birim(request.user)

        if birim:
            return qs.filter(demirbas__birim=birim)

        return qs.none()

    # 🔒 YETKİLER
    def has_add_permission(self, request):
        return is_admin(request.user)

    def has_change_permission(self, request, obj=None):
        return is_admin(request.user)

    def has_delete_permission(self, request, obj=None):
        return is_admin(request.user)