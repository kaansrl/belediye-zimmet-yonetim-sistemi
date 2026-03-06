# core/admin.py
from django.contrib import admin
from django.contrib.auth.models import User, Group
from django.contrib.auth.admin import UserAdmin as DjangoUserAdmin
from django.contrib.auth.admin import GroupAdmin as DjangoGroupAdmin

def is_admin(user):
    return user.is_superuser or user.groups.filter(name="Admin").exists()

class MyAdminSite(admin.AdminSite):
    site_header = "BDZYS Yönetim"
    site_title = "BDZYS Admin"
    index_title = "Site Yönetimi"

    def has_permission(self, request):
        user = request.user
        if not user.is_active:
            return False
        # Admin paneline girebilmek için staff şart + (Admin veya Birim Yetkilisi)
        return user.is_staff and (
            is_admin(user) or user.groups.filter(name="Birim Yetkilisi").exists()
        )

admin_site = MyAdminSite(name="myadmin")


# --- Auth modellerini bizim admin_site'a, DOĞRU admin sınıflarıyla bağla ---

@admin.register(User, site=admin_site)
class UserAdmin(DjangoUserAdmin):
    # User/Group modülünü sadece gerçek Admin görsün
    def has_module_permission(self, request):
        return is_admin(request.user)

@admin.register(Group, site=admin_site)
class GroupAdmin(DjangoGroupAdmin):
    def has_module_permission(self, request):
        return is_admin(request.user)