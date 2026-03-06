from django.urls import path
from .views import dashboard, export_aktif_zimmet_csv

urlpatterns = [
    path("", dashboard, name="raporlar_dashboard"),
    path("aktif-zimmet-csv/", export_aktif_zimmet_csv, name="export_aktif_zimmet_csv"),
]