# Generated by Django 4.0.3 on 2022-04-14 19:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('avisos', '0017_alter_car_name'),
    ]

    operations = [
        migrations.AddField(
            model_name='medicalrecord',
            name='no_medical_record',
            field=models.BooleanField(default=False),
        ),
    ]
