from rest_framework.serializers import ModelSerializer

from online_training.models import Course, Lesson


class CourseSerializer(ModelSerializer):
    class Meta:
        model = Course
        fields = (
            'name',
            'image',
            'description'
        )

class LessonSerializer(ModelSerializer):
    class Meta:
        model = Lesson
        fields = (
            'name',
            'image',
            'description',
            'video_url',
            'course'
        )