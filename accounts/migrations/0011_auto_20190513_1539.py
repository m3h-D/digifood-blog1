# Generated by Django 2.2 on 2019-05-13 11:09

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0010_auto_20190502_1433'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='phone',
            field=models.IntegerField(blank=True, null=True, validators=[django.core.validators.MinValueValidator(11)]),
        ),
    ]
