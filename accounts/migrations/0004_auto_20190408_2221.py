# Generated by Django 2.2 on 2019-04-08 17:51

from django.db import migrations
import django.db.models.manager


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0003_auto_20190408_2154'),
    ]

    operations = [
        migrations.AlterModelManagers(
            name='userprofile',
            managers=[
                ('test', django.db.models.manager.Manager()),
            ],
        ),
    ]
