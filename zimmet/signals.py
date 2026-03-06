# zimmet/signals.py
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils import timezone
from .models import ZimmetKaydi

@receiver(post_save, sender=ZimmetKaydi)
def zimmet_durum_guncelle(sender, instance, created, **kwargs):
    demirbas = instance.demirbas

    if instance.durum == "aktif":
        demirbas.durum = "zimmetli"
        demirbas.save(update_fields=["durum"])
        return

    if instance.durum == "iade":
        # iade_tarihi boşsa otomatik doldur (update ile, tekrar signal tetiklemesin)
        if not instance.iade_tarihi:
            ZimmetKaydi.objects.filter(pk=instance.pk).update(
                iade_tarihi=timezone.now().date()
            )

        demirbas.durum = "stokta"
        demirbas.save(update_fields=["durum"])