# Generated by Django 2.1.2 on 2018-12-07 21:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('calls', '0004_auto_20181207_1607'),
    ]

    operations = [
        migrations.AlterField(
            model_name='calls',
            name='calldate',
            field=models.DateTimeField(blank=True, default='2018-12-07 21:09:32'),
        ),
    ]