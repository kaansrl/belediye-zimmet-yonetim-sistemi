# zimmet/apps.py
from django.apps import AppConfig

class ZimmetConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "zimmet"

    def ready(self):
        from . import signals  # noqa