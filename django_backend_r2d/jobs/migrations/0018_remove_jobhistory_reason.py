# Generated by Django 5.0.1 on 2024-07-14 03:21

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('jobs', '0017_rename_model_name_jobqueue_model'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='jobhistory',
            name='reason',
        ),
    ]
