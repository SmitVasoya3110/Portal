# Generated by Django 4.2.10 on 2024-03-17 13:55

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('student', '0010_alter_question_unique_together'),
    ]

    operations = [
        migrations.CreateModel(
            name='Branch',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('branch_name', models.CharField(max_length=71)),
                ('college', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='student.college')),
            ],
        ),
    ]
