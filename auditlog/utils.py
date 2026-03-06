# auditlog/utils.py
from auditlog.middleware import get_current_request


def get_client_ip(request):
    if not request:
        return None
    xff = request.META.get("HTTP_X_FORWARDED_FOR")
    if xff:
        # "client, proxy1, proxy2"
        return xff.split(",")[0].strip()
    return request.META.get("REMOTE_ADDR")


def get_request_user(request):
    if not request:
        return None
    user = getattr(request, "user", None)
    if user and user.is_authenticated:
        return user
    return None


def get_user_birim_adi(user):
    """
    Senin projendeki KullaniciBirim modelinden birim adını çekmeye çalışır.
    Model yolunu projenizdeki gerçek yere göre ayarladım: envanter.models.KullaniciBirim
    """
    if not user:
        return ""
    try:
        from envanter.models import KullaniciBirim
        kb = (
            KullaniciBirim.objects.select_related("birim")
            .filter(kullanici=user)
            .first()
        )
        return kb.birim.ad if (kb and kb.birim) else ""
    except Exception:
        return ""


def get_audit_context():
    """
    Signals içinden çağır: user/ip/birim döndürür.
    """
    request = get_current_request()
    user = get_request_user(request)
    ip = get_client_ip(request)
    birim_adi = get_user_birim_adi(user)
    return user, ip, birim_adi