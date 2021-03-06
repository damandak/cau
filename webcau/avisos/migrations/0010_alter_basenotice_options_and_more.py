# Generated by Django 4.0.3 on 2022-06-25 17:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('avisos', '0009_globalsettings_group_mail_alter_friend_first_surname'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='basenotice',
            options={'ordering': ['status', '-max_end_date']},
        ),
        migrations.AddField(
            model_name='globalsettings',
            name='not_authorized_image',
            field=models.ImageField(blank=True, null=True, upload_to='avisos/not_authorized'),
        ),
        migrations.AlterField(
            model_name='basenotice',
            name='parking_location',
            field=models.CharField(blank=True, default='', max_length=100),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='emergencycontact',
            name='email',
            field=models.EmailField(blank=True, max_length=254, null=True),
        ),
        migrations.AlterField(
            model_name='emergencycontact',
            name='main_contact',
            field=models.BooleanField(default=True),
        ),
        migrations.AlterField(
            model_name='emergencycontact',
            name='name',
            field=models.CharField(default='', max_length=100),
            preserve_default=False,
        ),
    ]
