from django.db import models
from django.conf import settings


class Birim(models.Model):
    ad = models.CharField(max_length=150, unique=True)
    aciklama = models.TextField(blank=True, null=True)
    aktif = models.BooleanField(default=True)
    olusturma_tarihi = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Birim"
        verbose_name_plural = "Birimler"
        ordering = ["ad"]

    def __str__(self):
        return self.ad


class Personel(models.Model):
    ad_soyad = models.CharField(max_length=150)
    sicil_no = models.CharField(max_length=50, unique=True)
    gorev = models.CharField(max_length=100)
    birim = models.ForeignKey(Birim, on_delete=models.PROTECT)
    aktif = models.BooleanField(default=True)
    olusturma_tarihi = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Personel"
        verbose_name_plural = "Personeller"
        ordering = ["ad_soyad"]

    def __str__(self):
        return f"{self.ad_soyad} ({self.sicil_no})"


class Demirbas(models.Model):
    DURUM_SECENEKLERI = [
        ("stokta", "Stokta"),
        ("zimmetli", "Zimmetli"),
        ("arizali", "Arızalı"),
        ("hurda", "Hurda"),
    ]

    kod = models.CharField(max_length=100, unique=True)
    ad = models.CharField(max_length=150)
    kategori = models.CharField(max_length=100)
    seri_no = models.CharField(max_length=100, blank=True, null=True)
    marka_model = models.CharField(max_length=150, blank=True, null=True)
    satin_alma_tarihi = models.DateField(blank=True, null=True)
    birim = models.ForeignKey(Birim, on_delete=models.PROTECT)
    durum = models.CharField(max_length=20, choices=DURUM_SECENEKLERI, default="stokta")
    aciklama = models.TextField(blank=True, null=True)
    olusturma_tarihi = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Demirbaş"
        verbose_name_plural = "Demirbaşlar"
        ordering = ["kod"]

    def __str__(self):
        return f"{self.kod} - {self.ad}"


class KullaniciBirim(models.Model):
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="birim_bilgisi",
    )
    birim = models.ForeignKey(Birim, on_delete=models.PROTECT)

    class Meta:
        verbose_name = "Kullanıcı Birim Eşleştirmesi"
        verbose_name_plural = "Kullanıcı Birim Eşleştirmeleri"

    def __str__(self):
        return f"{self.user} -> {self.birim.ad}"