# Generated by Django 5.0.1 on 2024-06-25 15:41

import django.utils.timezone
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('jobs', '0008_rename_changed_timestamp_jobhistory_updated_timestamp_and_more'),
    ]

    operations = [
        migrations.RenameField(
            model_name='jobhistory',
            old_name='updated_timestamp',
            new_name='created_timestamp',
        ),
        migrations.RenameField(
            model_name='jobqueue',
            old_name='updated_timestamp',
            new_name='last_updated_timestamp',
        ),
        migrations.AddField(
            model_name='jobhistory',
            name='last_updated_timestamp',
            field=models.DateTimeField(auto_now=True),
        ),
        migrations.AddField(
            model_name='jobqueue',
            name='created_timestamp',
            field=models.DateTimeField(auto_now_add=True, default=django.utils.timezone.now),
            preserve_default=False,
        ),
    ]
