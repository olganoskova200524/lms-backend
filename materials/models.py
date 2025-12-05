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

    def __str__(self):
        return f'{self.title} ({self.course})'
