# Generated by Django 4.0.3 on 2022-06-27 13:57

from django.db import migrations, models
import django.db.models.deletion
import phonenumber_field.modelfields


class Migration(migrations.Migration):

    dependencies = [
        ('avisos', '0013_alter_car_member'),
    ]

    operations = [
        migrations.AlterField(
            model_name='friend',
            name='member',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='avisos.member'),
        ),
        migrations.AlterField(
            model_name='member',
            name='phone_number',
            field=phonenumber_field.modelfields.PhoneNumberField(blank=True, max_length=128, null=True, region=None),
        ),
    ]
