# Generated by Django 2.1.2 on 2018-11-25 16:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('experience', '0007_experience_pediste_info'),
    ]

    operations = [
        migrations.AlterField(
            model_name='experience',
            name='user',
            field=models.CharField(max_length=255),
        ),
    ]
