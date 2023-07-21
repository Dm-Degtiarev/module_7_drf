from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from online_training.models import Course, Lesson, Subscription
from user.models import User


class LessonTestCase(APITestCase):
    def setUp(self):
        self.user = User.objects.create(email='testuser@example.com', password='testpassword')
        self.client.force_authenticate(user=self.user)
        self.course = Course.objects.create(name='Test Course', author=self.user)
        self.lesson = Lesson.objects.create(name='TEST', description='TEST', video_url='https://www.youtube.com/', \
                                            course=self.course, author=self.user)
        self.data = {
            'name': 'TEST',
            'description': 'TEST',
            'video_url': 'https://www.youtube.com/',
            'course': self.course.id,
            'author': self.user.id,
        }

    def test_create_lesson(self):
        """Тестирование создания урока"""
        response = self.client.post(reverse('lesson_create'), data=self.data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.json(), {'id': 2, 'name': 'TEST', 'description': 'TEST', 'image': None, \
                                           'video_url': 'https://www.youtube.com/', 'course': 1, 'author': 1})
        self.assertTrue(Lesson.objects.all().exists())

    def test_list_lesson(self):
        """Тестирование вывода уроков"""
        response = self.client.get(reverse('lesson_list'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.json(), {
            "count": 1,
            "next": None,
            "previous": None,
            "results": [{'id': 1, 'name': 'TEST', 'description': 'TEST', 'image': None, \
                         'video_url': 'https://www.youtube.com/', 'course': 1, 'author': 1}]
            }
        )

    def test_lesson_retrieve(self):
        """Тестирование получение урока"""
        response = self.client.get(reverse('lesson_detail', kwargs={'pk': self.lesson.id}))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.json(), {'id': 1, 'name': 'TEST', 'description': 'TEST', 'image': None, \
                                           'video_url': 'https://www.youtube.com/', 'course': 1, 'author': 1})

    def test_lesson_destroy(self):
        """Тестирование удаления урока"""
        response = self.client.delete(reverse('lesson_delete', kwargs={'pk': self.lesson.id}))
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_lesson_update(self):
        """Тестирование обновления урока"""
        url = reverse('lesson_update', kwargs={'pk': self.lesson.id})
        response = self.client.patch(url, {'name': 'test'})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.json(), {'id': 1, 'name': 'test', 'description': 'TEST', 'image': None, \
                                           'video_url': 'https://www.youtube.com/', 'course': 1, 'author': 1})
        self.assertTrue(Lesson.objects.all().exists())

class SubscribeTestCase(APITestCase):
    def setUp(self):
        self.user = User.objects.create(email='testuser@example.com', password='testpassword')
        self.client.force_authenticate(user=self.user)
        self.course = Course.objects.create(name='Test Course', author=self.user)
        self.subscription = Subscription.objects.create(course=self.course, user=self.user, status=True)

        self.data = {
            'course': self.course.id,
            'user': self.user.id,
            'status': True,
        }

    def test_create_subscription(self):
        """Тестирование создания подписки"""
        response = self.client.post(reverse('subscription_create'), data=self.data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.json(), {'id': 2, 'course': 1, 'user': 1, 'status': True})
        self.assertTrue(Subscription.objects.all().exists())

    def test_list_subscription(self):
        """Тестирование вывода подписок"""
        response = self.client.get(reverse('subscription_list'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.json(), [{'id': 1, 'course': 1, 'user': 1, 'status': True}])

    def test_subscription_retrieve(self):
        """Тестирование получения подписки"""
        response = self.client.get(reverse('subscription_detail', kwargs={'pk': self.subscription.id}))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.json(), {'id': 1, 'course': 1, 'user': 1, 'status': True})

    def test_subscription_destroy(self):
        """Тестирование удаления подписки"""
        response = self.client.delete(reverse('subscription_delete', kwargs={'pk': self.subscription.id}))

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_subscription_update(self):
        """Тестирование обновления подписки"""
        url = reverse('subscription_update', kwargs={'pk': self.subscription.id})
        response = self.client.patch(url, {'status': False})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.json(), {'id': 1, 'course': 1, 'user': 1, 'status': False})
        self.assertTrue(Subscription.objects.all().exists())