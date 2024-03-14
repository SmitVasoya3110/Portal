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
admin.site.register(College)
# admin.site.register(ExamResult)
class ExamResultAdmin(admin.ModelAdmin):
    readonly_fields = ('user', 'student', 'exam', 'completed_at', 'score')
    list_display =  ('student', 'exam', 'score')
    # search_fields = ['user__email', 'student__enrollment_id', 'exam']
    def has_add_permission(self, request, obj=None):
        return False
    def has_change_permission(self, request, obj=None):
        return True
    def has_delete_permission(self, request, obj=None):
        return False


class StudentAdmin(admin.ModelAdmin):
    list_display =  ('user', 'college', 'branch', 'enrollment_id')
    # search_fields = ['user__email', 'college', 'branch', 'enrollment_id']
class ExamnAdmin(admin.ModelAdmin):
    list_display =  ('title', 'college', 'start_time')
    # search_fields = ['title', 'college']
class QuestionAdmin(admin.ModelAdmin):
    list_display =  ('question_text', 'exam', 'category')
    # search_fields = ['question_text', 'exam', 'category']

admin.site.register(Exam, ExamnAdmin)
admin.site.register(ExamResult, ExamResultAdmin)
admin.site.register(Question, QuestionAdmin)
# admin.site.register(Choice)
# admin.site.register(Record)
admin.site.register(Student, StudentAdmin)