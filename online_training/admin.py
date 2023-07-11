from django.contrib import admin
from online_training.models import Lesson, Payment, Course


@admin.register(Lesson)
class LessonAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')

@admin.register(Course)
class PaymentAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')

@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):
    list_display = ('date', 'course', 'user', 'paid', 'paid_method')
    search_fields = ('user', 'course')
    list_filter = ('user', 'course', 'date', 'paid_method')
