from django.contrib.auth.models import AbstractUser
from django.db.models import *


NULLABLE = {'null': True, 'blank': True}


class User(AbstractUser):
    username = None
    email = EmailField(unique=True, verbose_name='email')
    avatar = ImageField(upload_to='avatars', verbose_name='Аватар', **NULLABLE)
    phone_number = CharField(max_length=20, verbose_name='Номер телефона', **NULLABLE)
    country = CharField(max_length=100, verbose_name='Страна')

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    def __str__(self):
        return self.email