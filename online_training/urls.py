from django.urls import path
from rest_framework.routers import DefaultRouter
from .views import CourseViewSet, LessonUpdateView, LessonDetailView, LessonDeleteView, LessonCreateView, LessonListView, PaymentViewSet


course_router = DefaultRouter()
course_router.register(r'course', CourseViewSet, basename='course')
course_router.register(r'course/delete', CourseViewSet, basename='course_delete')

payment_router = DefaultRouter()
payment_router.register(r'payment', PaymentViewSet, basename='payment')


urlpatterns = [
      path('lesson/', LessonListView.as_view(), name='lesson_list'),
      path('lesson/create/', LessonCreateView.as_view(), name='lesson_create'),
      path('lesson/detail/<int:pk>/', LessonDetailView.as_view(), name='lesson_detail'),
      path('lesson/update/<int:pk>/', LessonUpdateView.as_view(), name='lesson_update'),
      path('lesson/delete/<int:pk>/', LessonDeleteView.as_view(), name='lesson_delete'),
] + course_router.urls + payment_router.urls