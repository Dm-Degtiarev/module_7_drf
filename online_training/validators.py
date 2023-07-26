from django.core.exceptions import ObjectDoesNotExist
from rest_framework import serializers
from online_training.models import Course, Payment


class VideoUrlValidator:
    def __init__(self, field):
        self.field = field

    def __call__(self, value):
        video_url = value.get('video_url')
        if video_url and 'youtube.com' not in video_url:
            raise serializers.ValidationError('URL должен быть с youtube.com')


class CourseValidator:
    def __init__(self, field):
        self.field = field

    def __call__(self, value):
        try:
            Course.objects.get(id=value)
        except ObjectDoesNotExist:
            raise serializers.ValidationError(f"Course with ID '{value}' not found")
        return value

class PaymentIntentValidator:
    def __init__(self, field):
        self.field = field

    def __call__(self, value):
        try:
            Payment.objects.get(intent_id=value)
        except ObjectDoesNotExist:
            raise serializers.ValidationError(f"Payment indent with ID '{value}' not found")
        return value