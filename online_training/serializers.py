from rest_framework import serializers
from online_training.models import Course, Lesson


class LessonSerializer(serializers.ModelSerializer):
    class Meta:
        model = Lesson
        fields = '__all__'


class CourseSerializer(serializers.ModelSerializer):
    lesson_count = serializers.SerializerMethodField(read_only=True)

    def get_lesson_count(self, obj):
        return obj.lesson_set.all().count()

    class Meta:
        model = Course
        fields = '__all__'