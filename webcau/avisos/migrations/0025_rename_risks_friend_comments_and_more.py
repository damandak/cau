# Generated by Django 4.0.3 on 2022-08-12 23:25

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('avisos', '0024_basenotice_arrival_conditions_and_more'),
    ]

    operations = [
        migrations.RenameField(
            model_name='friend',
            old_name='risks',
            new_name='comments',
        ),
        migrations.RenameField(
            model_name='medicalrecord',
            old_name='risks',
            new_name='comments',
        ),
    ]