# Generated by Django 4.2.6 on 2024-04-13 14:16

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0008_rename_computedmatch_computedmatch_computedmatchid'),
    ]

    operations = [
        migrations.AlterField(
            model_name='computedmatch',
            name='interviewID',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='core.interview'),
        ),
    ]