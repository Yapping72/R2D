# Generated by Django 5.0.1 on 2024-07-08 08:42

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('jobs', '0015_job_model_name_jobqueue_model_name'),
    ]

    operations = [
        migrations.RenameField(
            model_name='job',
            old_name='model_name',
            new_name='model',
        ),
    ]
