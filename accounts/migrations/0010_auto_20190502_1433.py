# Generated by Django 2.2 on 2019-05-02 10:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0009_auto_20190502_1324'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='phone',
            field=models.IntegerField(blank=True, null=True),
        ),
    ]
