# Generated by Django 3.2.2 on 2021-06-09 10:14

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('network', '0002_auto_20210524_1518'),
    ]

    operations = [
        migrations.AlterField(
            model_name='post',
            name='date',
            field=models.DateTimeField(default=datetime.datetime(2021, 6, 9, 16, 14, 21, 367417)),
        ),
        migrations.AlterUniqueTogether(
            name='profile',
            unique_together={('following', 'follower')},
        ),
    ]
