# Generated by Django 4.0.3 on 2022-06-24 14:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('avisos', '0006_alter_friend_emergencycontact_email_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='noticecategory',
            name='priority',
            field=models.IntegerField(default=0),
        ),
    ]