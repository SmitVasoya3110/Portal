# Generated by Django 4.2.10 on 2024-03-04 17:44

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('student', '0005_alter_choice_question'),
        ('teacher', '0002_teacher_id_alter_teacher_user'),
    ]

    operations = [
        migrations.AlterField(
            model_name='teacher',
            name='college',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='college', to='student.college'),
        ),
    ]
