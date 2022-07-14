# Generated by Django 4.0.3 on 2022-06-24 13:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('avisos', '0005_friend_medications_friend_risks_friend_sicknesses'),
    ]

    operations = [
        migrations.AlterField(
            model_name='friend',
            name='emergencycontact_email',
            field=models.EmailField(blank=True, max_length=254),
        ),
        migrations.AlterField(
            model_name='friend',
            name='emergencycontact_name',
            field=models.CharField(default='', max_length=100),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='friend',
            name='emergencycontact_relationship',
            field=models.CharField(blank=True, default='', max_length=100),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='friend',
            name='first_surname',
            field=models.CharField(blank=True, max_length=100),
        ),
        migrations.AlterField(
            model_name='friend',
            name='medications',
            field=models.CharField(blank=True, default='', max_length=100),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='friend',
            name='phone_number',
            field=models.CharField(blank=True, default='', max_length=20),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='friend',
            name='risks',
            field=models.CharField(blank=True, default='', max_length=100),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='friend',
            name='rut',
            field=models.CharField(blank=True, max_length=20),
        ),
        migrations.AlterField(
            model_name='friend',
            name='sicknesses',
            field=models.CharField(blank=True, default='', max_length=100),
            preserve_default=False,
        ),
    ]