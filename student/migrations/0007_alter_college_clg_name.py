# Generated by Django 4.2.10 on 2024-03-14 14:06

import django.contrib.postgres.fields.citext
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('student', '0006_alter_examresult_completed_at'),
    ]

    operations = [
        migrations.AlterField(
            model_name='college',
            name='clg_name',
            field=django.contrib.postgres.fields.citext.CICharField(max_length=300, unique=True),
        ),
    ]
