# Generated by Django 4.2.10 on 2024-03-17 14:42

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('student', '0014_alter_student_enrollment_id'),
        ('teacher', '0005_alter_teacher_user'),
    ]

    operations = [
        migrations.AlterField(
            model_name='teacher',
            name='branch',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='student.branch'),
        ),
    ]
