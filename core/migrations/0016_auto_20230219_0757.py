# Generated by Django 2.2.3 on 2023-02-19 07:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0015_auto_20230219_0750'),
    ]

    operations = [
        migrations.AlterField(
            model_name='item',
            name='wearing_part',
            field=models.CharField(choices=[('top_piece', 'Top Piece'), ('bottom_piece', 'Bottom Piece'), ('one_piece', 'One Piece')], default='top_piece', max_length=20),
        ),
    ]