# Generated by Django 2.1.2 on 2018-12-07 21:07

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('calls', '0003_auto_20181207_1548'),
    ]

    operations = [
        migrations.AlterField(
            model_name='calls',
            name='calldate',
            field=models.DateTimeField(blank=True, default=datetime.datetime(2018, 12, 7, 16, 7, 46, 299277)),
        ),
    ]