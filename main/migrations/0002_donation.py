# Generated by Django 2.2.11 on 2020-12-29 05:11

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Donation',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('donor_name', models.CharField(default='', max_length=50)),
                ('amount', models.IntegerField(default=100)),
                ('date', models.DateTimeField(default=datetime.datetime(2020, 12, 29, 5, 11, 41, 561159, tzinfo=utc))),
                ('message', models.TextField(blank=True, default='', max_length=1000)),
            ],
        ),
    ]
