# Generated by Django 3.0.3 on 2020-05-11 13:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0014_auto_20200427_1653'),
    ]

    operations = [
        migrations.AlterField(
            model_name='spokenlanguage',
            name='name',
            field=models.CharField(max_length=100, unique=True),
        ),
    ]
