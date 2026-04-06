from django.db import models
from django.utils import timezone
from django.core.exceptions import ValidationError
from envanter.models import Demirbas, Personel


class ZimmetKaydi(models.Model):
    DURUM = [
        ("aktif", "Aktif"),
        ("iade", "İade Edildi"),
    ]

    demirbas = models.ForeignKey(Demirbas, on_delete=models.PROTECT)
    personel = models.ForeignKey(Personel, on_delete=models.PROTECT)

    verilme_tarihi = models.DateField(default=timezone.now)
    iade_tarihi = models.DateField(blank=True, null=True)

    durum = models.CharField(max_length=10, choices=DURUM, default="aktif")
    aciklama = models.TextField(blank=True, null=True)

    olusturma_tarihi = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Zimmet Kaydı"
        verbose_name_plural = "Zimmet Kayıtları"
        ordering = ["-olusturma_tarihi"]

    def clean(self):
        if self.durum == "aktif" and self.demirbas_id:
            qs = ZimmetKaydi.objects.filter(demirbas=self.demirbas, durum="aktif")
            if self.pk:
                qs = qs.exclude(pk=self.pk)
            if qs.exists():
                raise ValidationError("Bu demirbaş zaten aktif zimmetli. Önce iade edilmelidir.")

    def save(self, *args, **kwargs):
        self.full_clean()
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.demirbas} -> {self.personel} ({self.durum})"