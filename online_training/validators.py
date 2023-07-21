from rest_framework import serializers


class VideoUrlValidator:
    def __init__(self, field):
        self.field = field

    def __call__(self, value):
        video_url = value.get('video_url')
        if video_url and 'youtube.com' not in video_url:
            raise serializers.ValidationError('URL должен быть с youtube.com')