# Generated by Django 4.2.10 on 2024-03-14 16:37

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('teacher', '0003_alter_teacher_college'),
    ]

    operations = [
        migrations.AddField(
            model_name='teacher',
            name='last_login',
            field=models.DateTimeField(default=django.utils.timezone.now),
        ),
    ]