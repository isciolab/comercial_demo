# Generated by Django 2.1.2 on 2018-12-07 20:48

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('calls', '0002_calls_calldate'),
    ]

    operations = [
        migrations.AlterField(
            model_name='calls',
            name='calldate',
            field=models.DateTimeField(blank=True, default=datetime.datetime(2018, 12, 7, 15, 48, 26)),
        ),
    ]
