# Generated by Django 4.0.3 on 2022-06-22 16:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('avisos', '0003_friend'),
    ]

    operations = [
        migrations.AddField(
            model_name='basenotice',
            name='friends',
            field=models.ManyToManyField(blank=True, to='avisos.friend'),
        ),
    ]
