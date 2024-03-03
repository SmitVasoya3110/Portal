from django.contrib import admin
from .models import CustomUser, Student, College, Exam, ExamResult, Question, Choice, Record
from django.contrib.auth.admin import UserAdmin

# Register your models here.
@admin.register(CustomUser)
class CustomUserAdmin(UserAdmin):
    list_display = (
        'id', 'first_name', 'last_name', 'email', 'is_active', 'is_teacher', 'is_student'
    )
    exclude = ["username"]
    ordering = ("id",)
admin.site.register(Student)
admin.site.register(College)
admin.site.register(Exam)
admin.site.register(ExamResult)
admin.site.register(Question)
admin.site.register(Choice)
admin.site.register(Record)