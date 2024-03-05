from django.contrib import admin
from .models import CustomUser, Student, College, Exam, ExamResult, Question, Choice, Record
from django.contrib.auth.admin import UserAdmin

# Register your models here.

class CustomUserAdmin(UserAdmin):
    model = CustomUser
    ordering = ('email',)
    list_display = ('email', 'first_name', 'last_name', 'is_teacher', 'is_superuser')
    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        ('Personal Info', {'fields': ('first_name', 'last_name')}),
        ('Permissions', {
            'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions'),
        }),
        ('Important dates', {'fields': ('last_login', 'date_joined')}),
    )
admin.site.register(CustomUser, CustomUserAdmin)
admin.site.register(Student)
admin.site.register(College)
admin.site.register(Exam)
admin.site.register(ExamResult)
admin.site.register(Question)
admin.site.register(Choice)
admin.site.register(Record)