# Generated by Django 2.1.4 on 2019-02-24 13:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('registration', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='customer',
            name='referee',
        ),
        migrations.AddField(
            model_name='person',
            name='cellphone_number',
            field=models.IntegerField(default=0, verbose_name='شماره تلفن همراه'),
            preserve_default=False,
        ),
    ]
