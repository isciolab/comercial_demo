# Generated by Django 2.1.2 on 2018-12-04 20:19

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('calls', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='calls',
            name='calldate',
            field=models.DateTimeField(blank=True, default=datetime.datetime.now),
        ),
    ]
