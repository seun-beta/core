# Generated by Django 3.0.7 on 2020-08-16 21:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0004_auto_20200816_1545'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='avatar',
            field=models.URLField(blank=True, default='https://avatars.githubusercontent.com/u/<userid>', null=True),
        ),
    ]