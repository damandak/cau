# Generated by Django 4.0.3 on 2022-07-14 21:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('avisos', '0021_remove_shortnotice_location_remove_shortnotice_route_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='globalsettings',
            name='notice_arrival_mail_content',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='globalsettings',
            name='notice_late_mail_content',
            field=models.TextField(blank=True, null=True),
        ),
    ]
