# Generated by Django 5.0.1 on 2024-07-14 05:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('diagrams', '0006_erdiagram'),
    ]

    operations = [
        migrations.AddField(
            model_name='classdiagram',
            name='controllers',
            field=models.JSONField(default='test'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='classdiagram',
            name='views',
            field=models.JSONField(default='tesst'),
            preserve_default=False,
        ),
    ]
