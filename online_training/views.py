from rest_framework import viewsets, generics
from online_training.models import Course, Lesson
from online_training.serializers import CourseSerializer


class CourseViewSet(viewsets.ViewSet):
    serializer_class = CourseSerializer
    queryset = Course.objects.all()