# Generated by Django 4.2.3 on 2023-07-08 07:24

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('online_training', '0002_rename_сourse_course'),
    ]

    operations = [
        migrations.RenameField(
            model_name='lesson',
            old_name='Course',
            new_name='course',
        ),
    ]
