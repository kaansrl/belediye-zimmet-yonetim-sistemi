# auditlog/services.py
from django.contrib.contenttypes.models import ContentType

from .models import AuditLog
from .middleware import get_current_request  # sende bu fonksiyon olmalı


def write_audit_log(action: str, instance, extra: dict | None = None):
    """
    action: 'create' | 'update' | 'delete'
    instance: kaydedilen/silinen model objesi
    """
    request = get_current_request()

    user = getattr(request, "user", None) if request else None
    if user and not user.is_authenticated:
        user = None

    ip = None
    if request:
        ip = request.META.get("REMOTE_ADDR")

    birim_adi = ""
    # instance üzerinde birim alanı varsa yakalamaya çalışalım
    # Demirbas.birim, Personel.birim, ZimmetKaydi.demirbas.birim gibi
    try:
        if hasattr(instance, "birim") and instance.birim:
            birim_adi = str(instance.birim)
        elif hasattr(instance, "demirbas") and instance.demirbas and instance.demirbas.birim:
            birim_adi = str(instance.demirbas.birim)
    except Exception:
        pass

    AuditLog.objects.create(
        action=action,
        model=instance.__class__.__name__,
        object_id=str(instance.pk),
        object_repr=str(instance),
        user=user,
        birim_adi=birim_adi,
        ip_address=ip,
        extra=extra or {},
    )