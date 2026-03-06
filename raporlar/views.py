from django.contrib.auth.decorators import login_required
from django.db.models import Count
from django.shortcuts import render
from django.http import HttpResponse
import csv

from envanter.models import Demirbas, KullaniciBirim
from zimmet.models import ZimmetKaydi


def _is_admin(user) -> bool:
    # Grup adın farklıysa burayı değiştir: "Admin"
    return user.is_superuser or user.groups.filter(name="Admin").exists()


def _get_user_birim(user):
    try:
        return KullaniciBirim.objects.select_related("birim").get(user=user).birim
    except KullaniciBirim.DoesNotExist:
        return None


def _get_filtered_querysets(request):
    user = request.user
    admin_mi = _is_admin(user)
    birim = _get_user_birim(user)

    demirbas_qs = Demirbas.objects.select_related("birim").all()
    zimmet_qs = ZimmetKaydi.objects.select_related(
        "demirbas", "demirbas__birim", "personel"
    ).all()

    # Admin değilse: sadece kendi birimi
    if not admin_mi:
        if birim is None:
            demirbas_qs = demirbas_qs.none()
            zimmet_qs = zimmet_qs.none()
        else:
            demirbas_qs = demirbas_qs.filter(birim=birim)
            zimmet_qs = zimmet_qs.filter(demirbas__birim=birim)

    # Tarih aralığı filtresi (opsiyonel)
    start = request.GET.get("start")  # YYYY-MM-DD
    end = request.GET.get("end")      # YYYY-MM-DD

    if start and end:
        zimmet_qs = zimmet_qs.filter(verilme_tarihi__range=[start, end])

    return {
        "user": user,
        "admin_mi": admin_mi,
        "birim": birim,
        "demirbas_qs": demirbas_qs,
        "zimmet_qs": zimmet_qs,
        "start": start or "",
        "end": end or "",
    }


@login_required
def dashboard(request):
    data = _get_filtered_querysets(request)

    demirbas_qs = data["demirbas_qs"]
    zimmet_qs = data["zimmet_qs"]

    # KPI sayıları
    kpi = {
        "zimmetli": demirbas_qs.filter(durum="zimmetli").count(),
        "stokta": demirbas_qs.filter(durum="stokta").count(),
        "arizali": demirbas_qs.filter(durum="arizali").count(),
        "hurda": demirbas_qs.filter(durum="hurda").count(),
        "toplam": demirbas_qs.count(),
    }

    # Grafik/tablo için dağılımlar
    kategori_dagilim = list(
        demirbas_qs.values("kategori")
        .annotate(adet=Count("id"))
        .order_by("-adet")
    )

    birim_dagilim = list(
        demirbas_qs.values("birim__ad")
        .annotate(adet=Count("id"))
        .order_by("-adet")
    )

    # Aktif zimmet listesi
    aktif_zimmetler = list(
        zimmet_qs.filter(durum="aktif").order_by("-verilme_tarihi")[:20]
    )

    ctx = {
        "admin_mi": data["admin_mi"],
        "is_admin": data["admin_mi"],
        "birim": data["birim"],
        "kpi": kpi,
        "kategori_dagilim": kategori_dagilim,
        "birim_dagilim": birim_dagilim,
        "aktif_zimmetler": aktif_zimmetler,
        "start": data["start"],
        "end": data["end"],
    }
    return render(request, "raporlar/dashboard.html", ctx)


@login_required
def export_aktif_zimmet_csv(request):
    data = _get_filtered_querysets(request)
    zimmet_qs = data["zimmet_qs"].filter(durum="aktif").order_by("-verilme_tarihi")

    response = HttpResponse(content_type="text/csv; charset=utf-8")
    response["Content-Disposition"] = 'attachment; filename="aktif_zimmetler.csv"'

    # Türkçe karakter sorunu yaşamamak için BOM ekliyoruz
    response.write("\ufeff")

    writer = csv.writer(response)
    writer.writerow([
        "Demirbaş Kodu",
        "Demirbaş Adı",
        "Personel",
        "Birim",
        "Veriliş Tarihi",
        "Durum",
        "Açıklama",
    ])

    for z in zimmet_qs:
        writer.writerow([
            z.demirbas.kod,
            z.demirbas.ad,
            z.personel.ad_soyad,
            z.demirbas.birim.ad if z.demirbas.birim else "",
            z.verilme_tarihi,
            z.durum,
            z.aciklama or "",
        ])

    return response