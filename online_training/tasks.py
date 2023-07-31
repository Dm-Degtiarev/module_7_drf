from datetime import timedelta
from config import settings
from online_training.models import Course, Subscription
from celery import shared_task
from django.core.mail import send_mail
from django.utils import timezone


@shared_task
def notify_course_updates(course_id):
    try:
        course = Course.objects.get(id=course_id)
    except Course.DoesNotExist:
        print(f"Курс с ID {course_id} не найден.")

    subscribers = Subscription.objects.filter(course=course_id, status=True)

    if course.last_update + timedelta(hours=4) <= timezone.now():
        subject = f'Курс {course.name} обновлён!'
        message = f'Проверьте курс {course.name}. В него добавлены новые материалы'
        sender_email = settings.EMAIL_HOST_USER

        for subscriber in subscribers:
            recipient_email = subscriber.user.email
            send_mail(subject, message, sender_email, [recipient_email], fail_silently=False)
            print(f'Отправлено на {recipient_email}')
    else:
        print(f'"{course.name}" был обновлен менее 4 часов назад!')

    course.last_update = timezone.now()
    course.save()