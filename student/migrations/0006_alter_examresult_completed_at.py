# Generated by Django 4.2.10 on 2024-03-13 17:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('student', '0005_alter_choice_question'),
    ]

    operations = [
        migrations.AlterField(
            model_name='examresult',
            name='completed_at',
            field=models.DateTimeField(auto_now_add=True),
        ),
    ]
