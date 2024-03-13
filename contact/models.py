from django.db import models

from student.forms import CustomUser
from pytz import timezone
# Create your models here.
class ContactUs(models.Model):
    username = models.CharField(max_length = 50)
    email = models.CharField(max_length = 50)
    message = models.TextField()
    replied = models.BooleanField(default=False)

    def __str__(self) -> str:
        return self.email
    
    class Meta:
        verbose_name = "Contact Us"
        verbose_name_plural = "Contact Us"

class Feedback(models.Model):
    username = models.CharField(max_length = 50)
    email = models.CharField(max_length = 50)
    message = models.TextField()
    rating = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True, null=True)

    def __str__(self) -> str:
        return self.email
    
class AdminReply(models.Model):
    contact_us = models.ForeignKey('ContactUs', on_delete=models.CASCADE)
    admin_user = models.ForeignKey(CustomUser, on_delete=models.SET_NULL, null=True, blank=True)
    reply_message = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Admin Reply"
        verbose_name_plural = "Admin Replies"

    def __str__(self):
        return f"Reply to {self.contact_us.email}"