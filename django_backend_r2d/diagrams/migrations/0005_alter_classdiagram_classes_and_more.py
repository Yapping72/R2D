# Generated by Django 5.0.1 on 2024-07-08 15:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('diagrams', '0004_rename_model_name_classdiagram_model'),
    ]

    operations = [
        migrations.AlterField(
            model_name='classdiagram',
            name='classes',
            field=models.JSONField(),
        ),
        migrations.AlterField(
            model_name='classdiagram',
            name='feature',
            field=models.JSONField(),
        ),
    ]
