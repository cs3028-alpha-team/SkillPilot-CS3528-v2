# Generated by Django 5.0.1 on 2024-04-14 14:02

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0007_recruiter_user'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='recruiter',
            name='user',
        ),
    ]