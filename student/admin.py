from django.contrib import admin
from .models import CustomUser, Student, College, Exam, ExamResult, Question, Choice, Record
from django.contrib.auth.admin import UserAdmin

# Register your models here.
admin.site.site_header = "Portal Admin"
admin.site.site_title = "Portal Admin"
admin.site.index_title = "Portal Admin"
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
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'password1', 'password2'),
        }),
    )

admin.site.register(CustomUser, CustomUserAdmin)
admin.site.register(Student)
admin.site.register(College)
admin.site.register(Exam)
# admin.site.register(ExamResult)
class ExamResultAdmin(admin.ModelAdmin):
    # readonly_fields = ('user', 'student', 'exam', 'completed_at')
    list_display =  ('student', 'exam', 'score')
    def has_add_permission(self, request, obj=None):
        return False
    def has_change_permission(self, request, obj=None):
        return True
    def has_delete_permission(self, request, obj=None):
        return False
admin.site.register(ExamResult, ExamResultAdmin)
admin.site.register(Question)
# admin.site.register(Choice)
# admin.site.register(Record)