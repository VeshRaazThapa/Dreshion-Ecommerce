# Generated by Django 2.2.3 on 2023-04-25 05:01

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0025_profile_label_image'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='profile',
            name='label_image',
        ),
    ]
