from rest_framework import serializers
from online_training.models import Course, Lesson, Payment, Subscription
from online_training.validators import VideoUrlValidator


class LessonSerializer(serializers.ModelSerializer):
    class Meta:
        model = Lesson
        fields = '__all__'
        validators = [VideoUrlValidator(field='video_url')]

class CourseSerializer(serializers.ModelSerializer):
    lesson_count = serializers.SerializerMethodField(read_only=True)
    lessons = LessonSerializer(many=True, read_only=True, source='lesson_set')
    subscription = serializers.SerializerMethodField()

    def get_lesson_count(self, obj):
        return obj.lesson_set.all().count()

    def get_subscription(self, obj):
        request = self.context.get('request')
        if request and request.user.is_authenticated:
            user = request.user
            course = obj
            subscription = Subscription.objects.filter(course=course, user=user).first()
            if subscription:
                return subscription.status
        return 'Not found'

    class Meta:
        model = Course
        fields = '__all__'

class PaymentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Payment
        fields = '__all__'

class SubscriptionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Subscription
        fields = '__all__'

