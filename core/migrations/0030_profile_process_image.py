# Generated by Django 2.2.3 on 2023-04-26 10:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0029_item_process_image'),
    ]

    operations = [
        migrations.AddField(
            model_name='profile',
            name='process_image',
            field=models.BooleanField(default=False),
        ),
    ]