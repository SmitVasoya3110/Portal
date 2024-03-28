from django.db import models

from student.models import Branch, CustomUser, College
from django.utils import timezone
# Create your models here.
class Teacher(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    teacher_id = models.IntegerField(default=1)
    college = models.ForeignKey(College, on_delete=models.CASCADE, related_name="college")
    branch = models.ForeignKey(Branch, on_delete=models.CASCADE)
    photo = models.ImageField(verbose_name="Photo", upload_to='teacher_photos', blank=True, null=True)
    last_login = models.DateTimeField(default=timezone.now)

    def save(self, *args, **kwargs):
        # This means that the model isn't saved to the database yet
        if self._state.adding:
            # Get the maximum display_id value from the database
            last_id = Teacher.objects.all().aggregate(largest=models.Max('teacher_id'))['largest']

            # aggregate can return None! Check it first.
            # If it isn't none, just use the last ID specified (which should be the greatest) and add one to it
            if last_id is not None:
                self.teacher_id = last_id + 1

        super(Teacher, self).save(*args, **kwargs)
    def __str__(self) -> str:
        return f"{self.user.email}-{self.user.first_name}-{self.user.last_name}"
    def __str__(self):
        return f"{self.user.get_full_name()} - {self.teacher_id}"