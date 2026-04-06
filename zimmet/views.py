from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from django.contrib.auth.decorators import login_required

from reportlab.pdfgen import canvas
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.lib.pagesizes import A4

from .models import ZimmetKaydi


pdfmetrics.registerFont(TTFont("ArialTR", r"C:\Windows\Fonts\arial.ttf"))
pdfmetrics.registerFont(TTFont("ArialTR-Bold", r"C:\Windows\Fonts\arialbd.ttf"))


def format_tarih(tarih):
    if not tarih:
        return "-"
    return tarih.strftime("%d.%m.%Y")


def format_durum(durum):
    mapping = {
        "aktif": "Aktif",
        "iade": "İade Edildi",
    }
    return mapping.get(durum, durum)


@login_required
def zimmet_pdf(request, zimmet_id):
    zimmet = get_object_or_404(ZimmetKaydi, id=zimmet_id)

    response = HttpResponse(content_type="application/pdf")
    response["Content-Disposition"] = f'attachment; filename="zimmet_{zimmet.id}.pdf"'

    p = canvas.Canvas(response, pagesize=A4)
    width, height = A4

    # Başlıklar
    p.setFont("ArialTR-Bold", 14)
    p.drawCentredString(width / 2, height - 50, "YEŞİLYURT BELEDİYESİ")

    p.setFont("ArialTR-Bold", 12)
    p.drawCentredString(width / 2, height - 70, "Demirbaş ve Zimmet Yönetim Sistemi")

    p.setFont("ArialTR-Bold", 20)
    p.drawCentredString(width / 2, height - 100, "ZİMMET FORMU")

    # Çizgi (biraz daha kalın hissi için)
    p.setLineWidth(1.2)
    p.line(60, height - 115, width - 60, height - 115)

    # İçerik
    y = height - 160
    sol_x = 80
    deger_x = 230

    alanlar = [
        ("Demirbaş Kodu:", zimmet.demirbas.kod),
        ("Demirbaş Adı:", zimmet.demirbas.ad),
        ("Personel:", zimmet.personel.ad_soyad),
        ("Birim:", zimmet.demirbas.birim.ad if zimmet.demirbas.birim else "-"),
        ("Verilme Tarihi:", format_tarih(zimmet.verilme_tarihi)),
        ("İade Tarihi:", format_tarih(zimmet.iade_tarihi)),
        ("Durum:", format_durum(zimmet.durum)),
        ("Açıklama:", zimmet.aciklama if zimmet.aciklama else "-"),
    ]

    for etiket, deger in alanlar:
        p.setFont("ArialTR-Bold", 12)
        p.drawString(sol_x, y, etiket)

        p.setFont("ArialTR", 12)
        p.drawString(deger_x, y, str(deger))
        y -= 30

    # İmza alanı
    y -= 40

    p.setFont("ArialTR-Bold", 12)
    p.drawString(80, y, "Teslim Alan")
    p.drawString(330, y, "Teslim Eden")

    y -= 50
    p.line(80, y, 250, y)
    p.line(330, y, 500, y)

    y -= 20
    p.setFont("ArialTR", 10)
    p.drawString(120, y, "İmza")
    p.drawString(380, y, "İmza")

    # Alt bilgi
    p.setFont("ArialTR", 9)
    p.drawString(80, 50, f"Zimmet Kayıt No: {zimmet.id}")

    p.showPage()
    p.save()

    return response