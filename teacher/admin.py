from django.contrib import admin
from .models import Teacher
from django.contrib.auth.models import Group


admin.site.unregister(Group)
# Register your models here.
admin.site.register(Teacher)