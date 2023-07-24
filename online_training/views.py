from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import viewsets, generics
from rest_framework.filters import OrderingFilter
from rest_framework.permissions import IsAuthenticated
from online_training.models import Course, Lesson, Payment, Subscription
from online_training.pagination import CoursePagination, LessonPagination
from online_training.permissions import ModeratorPermission, OwnerPermission
from online_training.serializers import CourseSerializer, LessonSerializer, PaymentSerializer, SubscriptionSerializer


# ViewSets
class CourseViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated, ModeratorPermission | OwnerPermission]
    serializer_class = CourseSerializer
    pagination_class = CoursePagination
    queryset = Course.objects.all()

    def get_queryset(self):
        user = self.request.user
        if user.groups.filter(name='Модератор').exists():
            return Course.objects.all()
        return Course.objects.filter(author=user)

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)


class PaymentViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
    serializer_class = PaymentSerializer
    queryset = Payment.objects.all()

    filter_backends = [DjangoFilterBackend, OrderingFilter]
    filterset_fields = ['course', 'paid_method']
    ordering_fields = ['date']

# Generics
class LessonListView(generics.ListCreateAPIView):
    permission_classes = [IsAuthenticated,  ModeratorPermission | OwnerPermission]
    serializer_class = LessonSerializer
    pagination_class = LessonPagination
    queryset = Lesson.objects.all()

    def get_queryset(self):
        user = self.request.user
        if user.groups.filter(name='Модератор').exists():
            return Lesson.objects.all()
        return Lesson.objects.filter(author=user)

    def post(self, request, *args, **kwargs):
        request.data["author"] = request.user.id
        return self.create(request, *args, **kwargs)


class LessonCreateView(generics.CreateAPIView):
    permission_classes = [IsAuthenticated,  ModeratorPermission | OwnerPermission]
    serializer_class = LessonSerializer
    queryset = Lesson.objects.all()

class LessonDeleteView(generics.DestroyAPIView):
    permission_classes = [IsAuthenticated, ModeratorPermission | OwnerPermission]
    serializer_class = LessonSerializer
    queryset = Lesson.objects.all()

class LessonDetailView(generics.RetrieveAPIView):
    permission_classes = [IsAuthenticated, OwnerPermission | ModeratorPermission]
    serializer_class = LessonSerializer
    queryset = Lesson.objects.all()

class LessonUpdateView(generics.UpdateAPIView):
    permission_classes = [IsAuthenticated, ModeratorPermission | OwnerPermission]
    serializer_class = LessonSerializer
    queryset = Lesson.objects.all()

class SubscriptionListView(generics.ListCreateAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = SubscriptionSerializer
    queryset = Subscription.objects.all()

class SubscriptionDetailView(generics.RetrieveAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = SubscriptionSerializer
    queryset = Subscription.objects.all()

class SubscriptionCreateView(generics.CreateAPIView):
    serializer_class = SubscriptionSerializer
    queryset = Subscription.objects.all()
    permission_classes = [IsAuthenticated]

class SubscriptionDeleteView(generics.DestroyAPIView):
    serializer_class = SubscriptionSerializer
    queryset = Subscription.objects.all()
    permission_classes = [IsAuthenticated]

class SubscriptionUpdateView(generics.UpdateAPIView):
    serializer_class = SubscriptionSerializer
    queryset = Subscription.objects.all()
    permission_classes = [IsAuthenticated]