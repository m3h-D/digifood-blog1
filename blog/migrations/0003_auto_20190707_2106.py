# Generated by Django 2.2 on 2019-07-07 16:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0002_auto_20190707_2102'),
    ]

    operations = [
        migrations.AddField(
            model_name='post',
            name='text2',
            field=models.TextField(blank=True),
        ),
        migrations.AddField(
            model_name='post',
            name='text3',
            field=models.TextField(blank=True),
        ),
        migrations.AddField(
            model_name='post',
            name='text4',
            field=models.TextField(blank=True),
        ),
        migrations.AddField(
            model_name='post',
            name='text5',
            field=models.TextField(blank=True),
        ),
    ]
