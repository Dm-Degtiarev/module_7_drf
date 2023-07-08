from django.db import models
from user.models import NULLABLE


class Course(models.Model):
    name = models.CharField(max_length=255, unique=True, verbose_name='Название')
    image = models.ImageField(verbose_name='Превью (картинка)', **NULLABLE)
    description = models.TextField(verbose_name='Описание', **NULLABLE)

class Lesson(models.Model):
    name = models.CharField(max_length=255, unique=True, verbose_name='Название')
    description = models.TextField(verbose_name='Описание', **NULLABLE)
    image = models.ImageField(verbose_name='Превью (картинка)', **NULLABLE)
    video_url = models.URLField(verbose_name='Ссылка на видео')
    course = models.ForeignKey('online_training.Course', on_delete=models.CASCADE, verbose_name='Курс')