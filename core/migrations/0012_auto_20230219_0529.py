# Generated by Django 2.2.3 on 2023-02-19 05:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0011_auto_20230219_0454'),
    ]

    operations = [
        migrations.CreateModel(
            name='DressType',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
            ],
        ),
        migrations.RemoveField(
            model_name='item',
            name='type',
        ),
    ]
