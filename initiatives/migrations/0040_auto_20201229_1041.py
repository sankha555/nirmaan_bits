# Generated by Django 2.2.11 on 2020-12-29 05:11

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('initiatives', '0039_auto_20200720_2158'),
    ]

    operations = [
        migrations.AlterField(
            model_name='initiativecomment',
            name='published_on',
            field=models.DateField(default=datetime.datetime(2020, 12, 29, 5, 11, 41, 558789, tzinfo=utc)),
        ),
    ]
