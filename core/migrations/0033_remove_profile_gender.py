# Generated by Django 2.2.3 on 2023-04-27 00:18

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0032_profile_gender'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='profile',
            name='gender',
        ),
    ]
