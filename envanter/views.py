from io import BytesIO

import qrcode
from PIL import Image, ImageDraw

from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.shortcuts import get_object_or_404

from .models import Demirbas


@login_required
def demirbas_qr(request, demirbas_id):
    demirbas = get_object_or_404(Demirbas, id=demirbas_id)

    qr_url = request.build_absolute_uri(
        f"/admin/envanter/demirbas/{demirbas.id}/change/"
    )

    # QR oluştur
    qr = qrcode.make(qr_url).convert("RGB")

    width, height = qr.size

    # Altına yazı alanı olan beyaz arka plan
    img = Image.new("RGB", (width, height + 60), (255, 255, 255))

    # QR'ı yapıştır
    img.paste(qr, (0, 0))

    # Yazı ekle
    draw = ImageDraw.Draw(img)
    text = f"{demirbas.kod} - {demirbas.ad}"
    draw.text((10, height + 20), text, fill=(0, 0, 0))

    # PNG olarak döndür
    buffer = BytesIO()
    img.save(buffer, format="PNG")
    buffer.seek(0)

    return HttpResponse(buffer.getvalue(), content_type="image/png")