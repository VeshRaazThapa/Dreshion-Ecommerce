# Generated by Django 2.2.3 on 2023-04-26 11:58

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0030_profile_process_image'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='profile',
            name='gender',
        ),
    ]
