from celery import shared_task
from django.core.mail import send_mail
from django.conf import settings

from materials.models import Course, Subscription


@shared_task
def notify_course_updated(course_id: int) -> dict:
    course = Course.objects.get(pk=course_id)

    emails = list(
        Subscription.objects.filter(course=course)
        .select_related("user")
        .values_list("user__email", flat=True)
    )

    if not emails:
        return {"sent": 0}

    subject = f"Курс обновлён: {course.title}"
    message = f"В курсе «{course.title}» появились обновления. Загляни в LMS 🙂"

    sent = send_mail(
        subject=subject,
        message=message,
        from_email=settings.DEFAULT_FROM_EMAIL,
        recipient_list=emails,
        fail_silently=False,
    )
    return {"sent": sent}
