# Generated by Django 2.2.11 on 2020-07-20 13:30

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('initiatives', '0036_auto_20200720_1854'),
    ]

    operations = [
        migrations.AlterField(
            model_name='initiativecomment',
            name='published_on',
            field=models.DateField(default=datetime.datetime(2020, 7, 20, 13, 30, 55, 6664, tzinfo=utc)),
        ),
    ]
