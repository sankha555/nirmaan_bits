# Generated by Django 2.2.11 on 2020-07-20 05:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0006_auto_20200719_1222'),
    ]

    operations = [
        migrations.AddField(
            model_name='visitor',
            name='message',
            field=models.TextField(blank=True, max_length=5000, null=True),
        ),
    ]
