from django.contrib import admin
from .models import Teacher
from django.contrib.auth.models import Group


admin.site.unregister(Group)
# Register your models here.

class TeacherAdmin(admin.ModelAdmin):
    model = Teacher
    list_display = ('user', 'teacher_id', 'college', 'branch', 'last_login')
    # fields = ('user', 'teacher_id', 'college', 'branch')

    def get_queryset(self, request):
        return super(TeacherAdmin,self).get_queryset(request).select_related('user')
    def teacher_login(self, obj):
        teacher = Teacher.objects.get(id=obj.id)
        return str(teacher.user.last_login)

    def last_login(self, obj):
        return obj.user.last_login

    def display_last_login(self, obj):
        return obj.user.last_login

    last_login.admin_order_field = 'last_login'    
    last_login.short_description = 'Last Login'    

    # fieldsets = (
    #     (None, {
    #         'fields': ('user', 'teacher_id', 'college', 'branch', 'last_login'),
    #     }),
    # )
admin.site.register(Teacher, TeacherAdmin)