# Generated by Django 5.0.1 on 2024-07-13 14:52

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('diagrams', '0005_alter_classdiagram_classes_and_more'),
        ('jobs', '0017_rename_model_name_jobqueue_model'),
        ('model_manager', '0003_update_model_names'),
    ]

    operations = [
        migrations.CreateModel(
            name='ERDiagram',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('feature', models.JSONField()),
                ('diagram', models.TextField()),
                ('description', models.TextField()),
                ('entities', models.JSONField()),
                ('is_audited', models.BooleanField(default=False)),
                ('created_timestamp', models.DateTimeField(auto_now_add=True)),
                ('last_updated_timestamp', models.DateTimeField(auto_now=True)),
                ('job', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='jobs.job')),
                ('model', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='model_manager.modelname')),
            ],
        ),
    ]
