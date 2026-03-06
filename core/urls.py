from django.contrib.auth import views as auth_views
from django.urls import path, include
from core.admin import admin_site
from .views import home

urlpatterns = [
    path("admin/", admin_site.urls),

    path(
        "login/",
        auth_views.LoginView.as_view(template_name="registration/login.html"),
        name="login",
    ),
    path("logout/", auth_views.LogoutView.as_view(), name="logout"),

    path("", home, name="home"),

    path("raporlar/", include("raporlar.urls")),
    path("zimmet/", include("zimmet.urls")),
    path("envanter/", include("envanter.urls")),
]