# Generated by Django 2.1.2 on 2018-11-07 01:48

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('experience', '0005_auto_20181106_0942'),
    ]

    operations = [
        migrations.RenameField(
            model_name='experience',
            old_name='user_id',
            new_name='user',
        ),
    ]
