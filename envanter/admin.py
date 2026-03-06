from django.contrib import admin
from django.utils.html import format_html
from django.urls import reverse

from .models import Birim, Personel, Demirbas, KullaniciBirim
from core.admin import admin_site


def is_admin(user):
    return user.is_superuser or user.groups.filter(name="Admin").exists()


def get_user_birim(user):
    kb = getattr(user, "birim_bilgisi", None)  # related_name = "birim_bilgisi" varsayımı
    return kb.birim if kb else None


@admin.register(KullaniciBirim, site=admin_site)
class KullaniciBirimAdmin(admin.ModelAdmin):
    list_display = ("user", "birim")
    search_fields = ("user__username", "user__email", "birim__ad")
    list_filter = ("birim",)

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
    list_display = ("ad", "aktif", "olusturma_tarihi")
    search_fields = ("ad",)
    list_filter = ("aktif",)

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
    list_display = ("ad_soyad", "sicil_no", "gorev", "birim", "aktif")
    search_fields = ("ad_soyad", "sicil_no")
    list_filter = ("birim", "aktif")

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
        "durum",
        "satin_alma_tarihi",
        "qr_gor",
    )
    search_fields = ("kod", "ad", "seri_no", "marka_model")
    list_filter = ("durum", "birim", "kategori")

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