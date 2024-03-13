from django.contrib.auth.models import AbstractUser
from django.db import models
from django.forms import ValidationError
from django.utils.translation import gettext_lazy as _
from pytz import timezone

from .managers import CustomUserManager


class CustomUser(AbstractUser):
    username = None
    email = models.EmailField(_("email address"), unique=True)
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
    is_student = models.BooleanField(default=False)
    is_teacher = models.BooleanField(default=False)
    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    objects = CustomUserManager()

    def __str__(self):
        return self.email
    
class College(models.Model):
    clg_name = models.CharField(max_length=300)
    address = models.TextField()

    def __str__(self):
        return self.clg_name
    
class Exam(models.Model):
    title = models.CharField(max_length=255)
    college = models.ForeignKey('College', on_delete=models.CASCADE)
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()

    def upcoming_exams(cls):
        # Implement logic to retrieve upcoming exams
        return cls.objects.filter(start_time__gte=timezone.now()).order_by('start_time')

    def __str__(self):
        return self.title

class Question(models.Model):
    CATEGORY = (
        ('Aptitude', 'Aptitude'),
        ('Programming', 'Programming')
    )
    exam = models.ForeignKey(Exam, on_delete=models.CASCADE, related_name='exam')
    question_text = models.TextField()
    category = models.CharField(max_length=30, choices=CATEGORY, default="None")


    def __str__(self):
        return self.question_text
    
class Choice(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE, related_name="choices")
    text = models.CharField(max_length=255)
    is_correct = models.BooleanField(default=False)

    def __str__(self):
        return self.text


class Student(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE, primary_key=True)
    college = models.ForeignKey(College, on_delete=models.CASCADE)
    enrollment_id = models.CharField(max_length=100, unique=True)
    branch = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self) -> str:
        return f"{self.user.email}-{self.user.first_name}-{self.user.last_name}"

class ExamResult(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    exam = models.ForeignKey(Exam, on_delete=models.CASCADE)
    completed_at = models.DateTimeField(auto_now_add=True)
    score = models.FloatField()

    def clean(self):
        if self.score < 0 or self.score > 100:
            raise ValidationError("Score must be between 0 and 100.")

    def __str__(self):
        return f"{self.student.user.get_full_name()} - {self.exam.title} - Score: {self.score}"

class Record(models.Model):
    student_id = models.CharField(max_length=10)
    exam_id = models.CharField(max_length=10)
    question_id = models.CharField(max_length=10)
    answer = models.CharField(max_length=1, default='N')
    created_at = models.DateTimeField(auto_now_add=True, null=True)
    updated_at = models.DateTimeField(auto_now=True, null=True)

    def __str__(self):
        return self.question_id + " : "+self.answer + "----Student_ID : " + self.student_id
      