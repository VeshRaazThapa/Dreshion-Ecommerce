# Generated by Django 2.2.3 on 2023-04-27 00:20

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0033_remove_profile_gender'),
    ]

    operations = [
        migrations.AddField(
            model_name='profile',
            name='gender',
            field=models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='core.Gender'),
        ),
    ]