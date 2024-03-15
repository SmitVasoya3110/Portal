from django.contrib import admin

from student.forms import CustomUser
from .models import Teacher
from django.contrib.auth.models import Group
from django.core.mail import send_mail
from django.conf import settings 

admin.site.unregister(Group)
# Register your models here.

class TeacherAdmin(admin.ModelAdmin):
    model = Teacher
    list_display = ('user', 'teacher_id', 'college', 'branch', 'last_login')
    # fields = ('user', 'teacher_id', 'college', 'branch')

    # def get_queryset(self, request):
    #     return super(TeacherAdmin,self).get_queryset(request).select_related('user')
    def teacher_login(self, obj):
        teacher = Teacher.objects.get(id=obj.id)
        return str(teacher.user.last_login)

    def last_login(self, obj):
        return obj.user.last_login

    def display_last_login(self, obj):
        return obj.user.last_login

    def save_model(self, request, obj, form, change):
        # Call the superclass method to save the object
        super().save_model(request, obj, form, change)

        # If a new teacher is created
        if not change:
            # Generate a random password
            password = CustomUser.objects.make_random_password()
            # Set the password for the user
            obj.user.set_password(password)
            obj.user.save()

            # Send an email containing the password
            send_mail(
                'Your account has been created',
                f'Your Email is: {obj.user.email}\nYour password is: {password}',
                settings.DEFAULT_FROM_EMAIL,
                [obj.user.email],
                fail_silently=False,
            )


    last_login.admin_order_field = 'last_login'    
    last_login.short_description = 'Last Login'    

    # fieldsets = (
    #     (None, {
    #         'fields': ('user', 'teacher_id', 'college', 'branch', 'last_login'),
    #     }),
    # )
admin.site.register(Teacher, TeacherAdmin)