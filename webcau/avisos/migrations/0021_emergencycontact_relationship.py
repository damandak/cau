# Generated by Django 4.0.3 on 2022-04-21 02:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('avisos', '0020_remove_emergencycontact_unique_main_contact_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='emergencycontact',
            name='relationship',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
    ]
