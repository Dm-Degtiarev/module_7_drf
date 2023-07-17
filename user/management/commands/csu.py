from django.core.management import BaseCommand
from user.models import User


# Команда создания суперюзера. Так как мы сделали вход по почте,
# при этом отменили по логину, который должен быть обязательно в методе созданию СЮ
class Command(BaseCommand):
    def handle(self, *args, **options):
        user = User.objects.create(
            email='moderator@django.ru',
            first_name='Admin',
            last_name='SkyPro',
            is_staff=False,
            is_superuser=False,
        )

        user.set_password('0001qwerty1000')
        user.save()
