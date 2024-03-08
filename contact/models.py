from django.db import models

# Create your models here.
class ContactUs(models.Model):
    username = models.CharField(max_length = 50)
    email = models.CharField(max_length = 50)
    message = models.TextField()

    def __str__(self) -> str:
        return self.email
    
    class Meta:
        verbose_name = "Contact Us"

class Feedback(models.Model):
    username = models.CharField(max_length = 50)
    email = models.CharField(max_length = 50)
    message = models.TextField()
    rating = models.IntegerField()

    def __str__(self) -> str:
        return self.email