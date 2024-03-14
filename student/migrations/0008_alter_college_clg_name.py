# Generated by Django 4.2.10 on 2024-03-14 14:12

from django.db import migrations
import student.models


class Migration(migrations.Migration):

    dependencies = [
        ('student', '0007_alter_college_clg_name'),
    ]

    operations = [
        migrations.AlterField(
            model_name='college',
            name='clg_name',
            field=student.models.CaseInsensitiveCharField(max_length=300, unique=True),
        ),
    ]
