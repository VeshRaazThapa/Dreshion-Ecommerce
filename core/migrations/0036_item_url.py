# Generated by Django 2.2.3 on 2023-06-07 11:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0035_auto_20230427_0025'),
    ]

    operations = [
        migrations.AddField(
            model_name='item',
            name='url',
            field=models.URLField(blank=True, help_text='Enter the URL.', null=True),
        ),
    ]