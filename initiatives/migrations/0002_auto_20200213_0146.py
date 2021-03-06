# Generated by Django 2.2 on 2020-02-12 20:16

import datetime
from django.db import migrations, models
import django.db.models.deletion
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('initiatives', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Post',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('published_on', models.DateField(default=datetime.datetime(2020, 2, 12, 20, 16, 26, 13734, tzinfo=utc))),
                ('title', models.CharField(default=None, max_length=255)),
                ('content', models.TextField(default='Foreign Key (type determined by related field)', max_length=1000)),
                ('likes', models.IntegerField(default=0)),
            ],
        ),
        migrations.AlterField(
            model_name='initiative',
            name='date_started',
            field=models.DateField(default=datetime.datetime(2020, 2, 12, 20, 16, 25, 985903, tzinfo=utc), verbose_name='Start Date'),
        ),
        migrations.CreateModel(
            name='PostComments',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('published_on', models.DateField(default=datetime.datetime(2020, 2, 12, 20, 16, 26, 14400, tzinfo=utc))),
                ('message', models.TextField(default='', max_length=255)),
                ('post', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='initiatives.Post')),
            ],
        ),
        migrations.AddField(
            model_name='post',
            name='initiative',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='initiatives.Initiative'),
        ),
    ]
