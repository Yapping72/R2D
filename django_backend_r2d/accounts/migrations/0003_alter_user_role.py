# Generated by Django 5.0.1 on 2024-05-22 05:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0002_alter_user_role'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='role',
            field=models.CharField(choices=[('NORMAL_USER', 'Normal User'), ('PAID_USER', 'Paid User'), ('IT_ADMINISTRATOR', 'IT Administrator'), ('ROOT', 'Root')], default='NORMAL_USER', max_length=50),
        ),
    ]
