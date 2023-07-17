from django.db import models
from user.models import NULLABLE
from datetime import date

class Course(models.Model):
    name = models.CharField(max_length=255, unique=True, verbose_name='Название')
    image = models.ImageField(upload_to='course', verbose_name='Превью (картинка)', **NULLABLE)
    description = models.TextField(verbose_name='Описание', **NULLABLE)
    author = models.ForeignKey("user.User", on_delete=models.SET_NULL, verbose_name='Автор', null=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Курс'
        verbose_name_plural = 'Курсы'

class Lesson(models.Model):
    name = models.CharField(max_length=255, verbose_name='Название')
    description = models.TextField(verbose_name='Описание', **NULLABLE)
    image = models.ImageField(upload_to='lesson', verbose_name='Превью (картинка)', **NULLABLE)
    video_url = models.URLField(verbose_name='Ссылка на видео')
    course = models.ForeignKey(Course, on_delete=models.CASCADE, verbose_name='Курс')
    author = models.ForeignKey("user.User", on_delete=models.SET_NULL, verbose_name='Автор', null=True)

    def __str__(self):
        return f"{self.course} - {self.name}"

    class Meta:
        verbose_name = 'Урок'
        verbose_name_plural = 'Уроки'

class Payment(models.Model):
    PAID_METHOD = (
        ('Сashless', 'Безналичный расчет'),
        ('Cash', 'Наличными')
    )

    user = models.ForeignKey('user.User', on_delete=models.SET_DEFAULT, default='', verbose_name='Пользователь')
    date = models.DateField(default=date.today, verbose_name='Дата платежа')
    course = models.ForeignKey(Course, on_delete=models.SET_NULL, null=True, verbose_name='Оплаченный курс')
    paid = models.FloatField(verbose_name='Cумма оплаты')
    paid_method = models.CharField(max_length=20, verbose_name='Способ оплаты', choices=PAID_METHOD)

    def __str__(self):
        return f"{self.user} - {self.course} - {self.date}"

    class Meta:
        verbose_name='Платеж'
        verbose_name_plural='Платежи'
