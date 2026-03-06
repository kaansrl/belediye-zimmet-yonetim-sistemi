from django.urls import path
from .views import zimmet_pdf

urlpatterns = [
    path("pdf/<int:zimmet_id>/", zimmet_pdf, name="zimmet_pdf"),
]