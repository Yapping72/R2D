# Generated by Django 5.0.1 on 2024-07-14 05:38

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('diagrams', '0007_classdiagram_controllers_classdiagram_views'),
    ]

    operations = [
        migrations.RenameField(
            model_name='classdiagram',
            old_name='controllers',
            new_name='helper_classes',
        ),
        migrations.RemoveField(
            model_name='classdiagram',
            name='views',
        ),
    ]
