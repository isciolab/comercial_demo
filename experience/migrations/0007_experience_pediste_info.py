# Generated by Django 2.1.2 on 2018-11-07 21:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('experience', '0006_auto_20181106_2048'),
    ]

    operations = [
        migrations.AddField(
            model_name='experience',
            name='pediste_info',
            field=models.BooleanField(default=0),
            preserve_default=False,
        ),
    ]
