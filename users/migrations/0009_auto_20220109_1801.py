# Generated by Django 3.2.9 on 2022-01-09 16:01

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0008_auto_20220105_2033'),
    ]

    operations = [
        migrations.AlterField(
            model_name='property_registration',
            name='detail',
            field=models.TextField(default='', max_length=250),
        ),
        migrations.AlterField(
            model_name='request_property',
            name='time_done',
            field=models.DateTimeField(default=datetime.datetime(2022, 1, 9, 16, 1, 22, 187763, tzinfo=utc)),
        ),
    ]