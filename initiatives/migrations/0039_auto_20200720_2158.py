# Generated by Django 2.2.11 on 2020-07-20 16:28

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('initiatives', '0038_auto_20200720_1905'),
    ]

    operations = [
        migrations.AlterField(
            model_name='initiativecomment',
            name='published_on',
            field=models.DateField(default=datetime.datetime(2020, 7, 20, 16, 28, 15, 678733, tzinfo=utc)),
        ),
    ]
