# Generated by Django 4.0.3 on 2022-07-11 20:08

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('avisos', '0017_basenotice_waiting_task_one_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='basenotice',
            name='max_end_date',
            field=models.DateTimeField(blank=True, default=datetime.datetime(2022, 7, 11, 20, 8, 50, 887937, tzinfo=utc)),
        ),
        migrations.AlterField(
            model_name='basenotice',
            name='start_date',
            field=models.DateTimeField(blank=True, default=datetime.datetime(2022, 7, 11, 20, 8, 50, 887917, tzinfo=utc)),
        ),
    ]
