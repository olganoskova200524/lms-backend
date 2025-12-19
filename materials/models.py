from django.conf import settings
from django.db import models


class Course(models.Model):
    title = models.CharField(max_length=255, verbose_name='название')
    description = models.TextField(blank=True, verbose_name='описание')
    preview = models.ImageField(
        upload_to='courses_previews/',
        blank=True,
        null=True,
        verbose_name='превью'
    )

    owner = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='courses',
        verbose_name='владелец'
    )

    def __str__(self):
        return self.title


class Lesson(models.Model):
    course = models.ForeignKey(
        Course,
        related_name='lessons',
        on_delete=models.CASCADE,
        verbose_name='курс'
    )
    title = models.CharField(max_length=255, verbose_name='название')
    description = models.TextField(blank=True, verbose_name='описание')
    preview = models.ImageField(
        upload_to='lessons_previews/',
        blank=True,
        null=True,
        verbose_name='превью'
    )
    video_url = models.URLField(verbose_name='ссылка на видео')

    owner = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='lessons',
        verbose_name='владелец'
    )

    def __str__(self):
        return f'{self.title} ({self.course})'


class Subscription(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='subscriptions',
        verbose_name='пользователь',
    )
    course = models.ForeignKey(
        'Course',
        on_delete=models.CASCADE,
        related_name='subscriptions',
        verbose_name='курс',
    )
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='создано')

    class Meta:
        verbose_name = 'подписка'
        verbose_name_plural = 'подписки'
        constraints = [
            models.UniqueConstraint(
                fields=['user', 'course'],
                name='unique_user_course_subscription',
            )
        ]

    def __str__(self):
        return f'{self.user} -> {self.course}'
