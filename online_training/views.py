from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import viewsets, generics
from rest_framework.filters import OrderingFilter
from rest_framework.permissions import IsAuthenticated
from online_training.models import Course, Lesson, Payment
from online_training.permissions import ModeratorPermission
from online_training.serializers import CourseSerializer, LessonSerializer, PaymentSerializer


# ViewSets
class CourseViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated, ModeratorPermission]
    serializer_class = CourseSerializer
    queryset = Course.objects.all()

class PaymentViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
    serializer_class = PaymentSerializer
    queryset = Payment.objects.all()

    filter_backends = [DjangoFilterBackend, OrderingFilter]
    filterset_fields = ['course', 'paid_method']
    ordering_fields = ['date']

# Generics
class LessonListView(generics.ListCreateAPIView):
    permission_classes = [IsAuthenticated, ModeratorPermission]
    serializer_class = LessonSerializer
    queryset = Lesson.objects.all()

class LessonCreateView(generics.CreateAPIView):
    permission_classes = [IsAuthenticated, ModeratorPermission]
    serializer_class = LessonSerializer
    queryset = Lesson.objects.all()

class LessonDeleteView(generics.DestroyAPIView):
    permission_classes = [IsAuthenticated, ModeratorPermission]
    serializer_class = LessonSerializer
    queryset = Lesson.objects.all()

class LessonDetailView(generics.RetrieveAPIView):
    permission_classes = [IsAuthenticated, ModeratorPermission]
    serializer_class = LessonSerializer
    queryset = Lesson.objects.all()

class LessonUpdateView(generics.UpdateAPIView):
    permission_classes = [IsAuthenticated, ModeratorPermission]
    serializer_class = LessonSerializer
    queryset = Lesson.objects.all()