from django.contrib import admin
from online_training.models import Lesson, Payment, Course
from user.models import User


@admin.register(Lesson)
class LessonAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'author')

@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'author')

@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):
    list_display = ('date', 'course', 'user', 'paid', 'paid_method')
    search_fields = ('user', 'course')
    list_filter = ('user', 'course', 'date', 'paid_method')

@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ('email', 'first_name', 'last_name', 'avatar', 'phone_number', 'country')


