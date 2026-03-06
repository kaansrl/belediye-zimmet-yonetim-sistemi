from django.urls import path
from .views import demirbas_qr

urlpatterns = [
    path("qr/<int:demirbas_id>/", demirbas_qr, name="demirbas_qr"),
]