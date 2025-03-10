# Generated by Django 5.0.1 on 2024-07-14 08:55

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('diagrams', '0008_rename_controllers_classdiagram_helper_classes_and_more'),
        ('jobs', '0020_alter_jobhistory_previous_status'),
        ('model_manager', '0003_update_model_names'),
    ]

    operations = [
        migrations.CreateModel(
            name='SequenceDiagram',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('feature', models.CharField(max_length=255)),
                ('diagram', models.TextField()),
                ('description', models.TextField()),
                ('actors', models.JSONField()),
                ('messages', models.JSONField()),
                ('alt_flows', models.JSONField(blank=True, null=True)),
                ('loops', models.JSONField(blank=True, null=True)),
                ('is_audited', models.BooleanField(default=False)),
                ('created_timestamp', models.DateTimeField(auto_now_add=True)),
                ('last_updated_timestamp', models.DateTimeField(auto_now=True)),
                ('job', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='jobs.job')),
                ('model', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='model_manager.modelname')),
            ],
        ),
    ]
