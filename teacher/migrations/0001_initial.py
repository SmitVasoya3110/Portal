# Generated by Django 4.2.10 on 2024-03-01 17:23

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('student', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Teacher',
            fields=[
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, primary_key=True, serialize=False, to=settings.AUTH_USER_MODEL)),
                ('teacher_id', models.CharField(max_length=100, unique=True)),
                ('branch', models.CharField(max_length=51)),
                ('college', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='student.college')),
            ],
        ),
    ]
