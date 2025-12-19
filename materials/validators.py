from urllib.parse import urlparse

from rest_framework.serializers import ValidationError


ALLOWED_HOSTS = {"youtube.com", "www.youtube.com"}


def validate_youtube_url(value: str) -> str:
    """
    Разрешаем ссылки только на YouTube.
    Запрещаем любые другие домены.
    """
    if not value:
        return value

    parsed = urlparse(value)
    host = (parsed.netloc or "").lower()

    if host not in ALLOWED_HOSTS:
        raise ValidationError("Можно добавлять ссылки только на youtube.com.")

    return value