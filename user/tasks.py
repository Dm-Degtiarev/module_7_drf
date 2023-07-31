from datetime import timedelta
from user.models import User
from django.utils import timezone
from celery import shared_task


@shared_task
def check_inactive_users():
    # Определяем период неактивности
    inactive_period = timezone.now() - timedelta(days=90)
    # Получаем список пользователей, которые не заходили более месяца и активны
    inactive_users = User.objects.filter(last_login__lt=inactive_period, is_active=True)
    # Блокируем пользователей, устанавливая флаг is_active в False
    for user in inactive_users:
        if user.is_superuser:
            continue
        user.is_active = False
        user.save()

    print(f"Заблокировано {inactive_users.count()} пользователей.")