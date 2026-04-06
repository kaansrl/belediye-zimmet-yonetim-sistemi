from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from django.contrib.auth import get_user_model

from envanter.models import Demirbas, Personel
from zimmet.models import ZimmetKaydi

from .models import AuditLog
from .services import write_audit_log

User = get_user_model()


@receiver(post_save, sender=Demirbas)
def log_demirbas_save(sender, instance, created, **kwargs):
    write_audit_log(
        AuditLog.ACTION_CREATE if created else AuditLog.ACTION_UPDATE,
        instanceassess
    )


@receiver(post_delete, sender=Demirbas)
def log_demirbas_delete(sender, instance, **kwargs):
    write_audit_log(AuditLog.ACTION_DELETE, instance)


@receiver(post_save, sender=Personel)
def log_personel_save(sender, instance, created, **kwargs):
    write_audit_log(
        AuditLog.ACTION_CREATE if created else AuditLog.ACTION_UPDATE,
        instance
    )


@receiver(post_delete, sender=Personel)
def log_personel_delete(sender, instance, **kwargs):
    write_audit_log(AuditLog.ACTION_DELETE, instance)


@receiver(post_save, sender=ZimmetKaydi)
def log_zimmet_save(sender, instance, created, **kwargs):
    write_audit_log(
        AuditLog.ACTION_CREATE if created else AuditLog.ACTION_UPDATE,
        instance
    )


@receiver(post_delete, sender=ZimmetKaydi)
def log_zimmet_delete(sender, instance, **kwargs):
    write_audit_log(AuditLog.ACTION_DELETE, instance)


# ✅ USER (oluşturma / güncelleme / pasif yapma)
@receiver(post_save, sender=User)
def log_user_save(sender, instance, created, **kwargs):
    write_audit_log(
        AuditLog.ACTION_CREATE if created else AuditLog.ACTION_UPDATE,
        instance
    )


@receiver(post_delete, sender=User)
def log_user_delete(sender, instance, **kwargs):
    write_audit_log(AuditLog.ACTION_DELETE, instance)