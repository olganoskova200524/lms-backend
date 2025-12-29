from datetime import timedelta

from celery import shared_task
from django.contrib.auth import get_user_model
from django.utils import timezone


@shared_task
def deactivate_inactive_users(days: int = 30) -> int:
    """
    Деактивирует пользователей, которые не входили в систему
    более `days` дней.
    Возвращает количество деактивированных пользователей.
    """
    User = get_user_model()
    cutoff = timezone.now() - timedelta(days=days)

    qs = (
        User.objects
        .filter(is_active=True, last_login__lt=cutoff)
        .exclude(is_superuser=True)
        .exclude(is_staff=True)
    )
    updated = qs.update(is_active=False)
    return updated
