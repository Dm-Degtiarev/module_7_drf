from django.urls import path
from rest_framework.routers import DefaultRouter
from .views import CourseViewSet, LessonUpdateView, LessonDetailView, LessonDeleteView, LessonCreateView, \
      LessonListView, PaymentViewSet, SubscriptionCreateView, SubscriptionDeleteView, SubscriptionUpdateView, \
      SubscriptionDetailView, SubscriptionListView

# Course
course_router = DefaultRouter()
course_router.register(r'course', CourseViewSet, basename='course')
course_router.register(r'course/delete', CourseViewSet, basename='course_delete')
course_router.register(r'course/detail', CourseViewSet, basename='course_detail')
course_router.register(r'course/update', CourseViewSet, basename='course_update')

# payment
payment_router = DefaultRouter()
payment_router.register(r'payment', PaymentViewSet, basename='payment')


urlpatterns = [
      path('lesson/', LessonListView.as_view(), name='lesson_list'),
      path('lesson/create/', LessonCreateView.as_view(), name='lesson_create'),
      path('lesson/detail/<int:pk>/', LessonDetailView.as_view(), name='lesson_detail'),
      path('lesson/update/<int:pk>/', LessonUpdateView.as_view(), name='lesson_update'),
      path('lesson/delete/<int:pk>/', LessonDeleteView.as_view(), name='lesson_delete'),
      path('subscription/', SubscriptionListView.as_view(), name='subscription_list'),
      path('subscription/create/', SubscriptionCreateView.as_view(), name='subscription_create'),
      path('subscription/detail/<int:pk>/', SubscriptionDetailView.as_view(), name='subscription_detail'),
      path('subscription/delete/<int:pk>/', SubscriptionDeleteView.as_view(),name='subscription_delete'),
      path('subscription/update/<int:pk>/', SubscriptionUpdateView.as_view(), name='subscription_update')
] + course_router.urls + payment_router.urls