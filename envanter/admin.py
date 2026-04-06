from django.contrib import admin
from django.utils.html import format_html
from django.urls import reverse

from .models import Birim, Personel, Demirbas, KullaniciBirim
from core.admin import admin_site


def is_admin(user):
    return user.is_superuser or user.groups.filter(name="Admin").exists()


def get_user_birim(user):
    kb = getattr(user, "birim_bilgisi", None)
    return kb.birim if kb else None


@admin.register(KullaniciBirim, site=admin_site)
class KullaniciBirimAdmin(admin.ModelAdmin):
    list_display = ("user", "birim")
    search_fields = ("user__username", "user__email", "birim__ad")
    list_filter = ("birim",)
    list_per_page = 20
    list_select_related = ("user", "birim")

    def has_module_permission(self, request):
        return is_admin(request.user)

    def has_view_permission(self, request, obj=None):
        return is_admin(request.user)

    def has_add_permission(self, request):
        return is_admin(request.user)

    def has_change_permission(self, request, obj=None):
        return is_admin(request.user)

    def has_delete_permission(self, request, obj=None):
        return is_admin(request.user)

@admin.register(Birim, site=admin_site)
class BirimAdmin(admin.ModelAdmin):
    list_display = ("ad", "aktif_durumu", "olusturma_tarihi")
    search_fields = ("ad",)
    list_filter = ("aktif",)
    list_per_page = 20
    ordering = ("ad",)
    readonly_fields = ("olusturma_tarihi",)

    def aktif_durumu(self, obj):
        return "Aktif" if obj.aktif else "Pasif"
    aktif_durumu.short_description = "Durum"

    def has_module_permission(self, request):
        return is_admin(request.user)

    def has_view_permission(self, request, obj=None):
        return is_admin(request.user)

    def has_add_permission(self, request):
        return is_admin(request.user)

    def has_change_permission(self, request, obj=None):
        return is_admin(request.user)

    def has_delete_permission(self, request, obj=None):
        return is_admin(request.user)


@admin.register(Personel, site=admin_site)
class PersonelAdmin(admin.ModelAdmin):
    list_display = ("ad_soyad", "sicil_no", "gorev", "birim", "aktif_durumu")
    search_fields = ("ad_soyad", "sicil_no", "gorev")
    list_filter = ("birim", "aktif")
    list_per_page = 20
    ordering = ("ad_soyad",)
    list_select_related = ("birim",)
    readonly_fields = ("olusturma_tarihi",)

    def aktif_durumu(self, obj):
        return "Aktif" if obj.aktif else "Pasif"
    aktif_durumu.short_description = "Durum"

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        if is_admin(request.user):
            return qs
        birim = get_user_birim(request.user)
        return qs.filter(birim=birim) if birim else qs.none()

    def has_add_permission(self, request):
        return is_admin(request.user)

    def has_change_permission(self, request, obj=None):
        return is_admin(request.user)

    def has_delete_permission(self, request, obj=None):
        return is_admin(request.user)


@admin.register(Demirbas, site=admin_site)
class DemirbasAdmin(admin.ModelAdmin):
    list_display = (
        "kod",
        "ad",
        "kategori",
        "birim",
        "durum_rozeti",
        "satin_alma_tarihi",
        "qr_gor",
    )
    search_fields = ("kod", "ad", "seri_no", "marka_model", "kategori")
    list_filter = ("durum", "birim", "kategori")
    list_per_page = 20
    ordering = ("kod",)
    list_select_related = ("birim",)
    readonly_fields = ("olusturma_tarihi",)

    def durum_rozeti(self, obj):
        renkler = {
            "stokta": "#198754",
            "zimmetli": "#0d6efd",
            "arizali": "#fd7e14",
            "hurda": "#dc3545",
        }
        etiketler = {
            "stokta": "Stokta",
            "zimmetli": "Zimmetli",
            "arizali": "Arızalı",
            "hurda": "Hurda",
        }
        renk = renkler.get(obj.durum, "#6c757d")
        etiket = etiketler.get(obj.durum, obj.durum)
        return format_html(
            '<span style="padding:4px 10px; border-radius:999px; color:white; background:{}; font-weight:600;">{}</span>',
            renk,
            etiket,
        )
    durum_rozeti.short_description = "Durum"

    def qr_gor(self, obj):
        url = reverse("demirbas_qr", args=[obj.id])
        return format_html(
            '<a class="button" href="{}" target="_blank">QR Gör</a> '
            '<a class="button" href="{}" download>İndir</a>',
            url,
            url,
        )
    qr_gor.short_description = "QR Kod"

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        if is_admin(request.user):
            return qs
        birim = get_user_birim(request.user)
        return qs.filter(birim=birim) if birim else qs.none()

    def has_add_permission(self, request):
        return is_admin(request.user)

    def has_change_permission(self, request, obj=None):
        return is_admin(request.user)

    def has_delete_permission(self, request, obj=None):
        return is_admin(request.user)