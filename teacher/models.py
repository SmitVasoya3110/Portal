from django.db import models

from student.models import CustomUser, College
from django.utils import timezone
# Create your models here.
class Teacher(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    teacher_id = models.CharField(max_length=100, unique=True)
    college = models.ForeignKey(College, on_delete=models.CASCADE, related_name="college")
    branch = models.CharField(max_length=51)
    last_login = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f"{self.user.get_full_name()} - {self.teacher_id}"