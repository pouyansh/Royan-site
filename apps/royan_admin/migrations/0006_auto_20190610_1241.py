# Generated by Django 2.1.7 on 2019-06-10 12:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('royan_admin', '0005_auto_20190609_1108'),
    ]

    operations = [
        migrations.AlterField(
            model_name='royantucagene',
            name='instagram',
            field=models.URLField(blank=True, default='', null=True, verbose_name='اینستاگرام'),
        ),
        migrations.AlterField(
            model_name='royantucagene',
            name='telegram',
            field=models.URLField(blank=True, default='', null=True, verbose_name='تلگرام'),
        ),
        migrations.AlterField(
            model_name='royantucagene',
            name='twitter',
            field=models.URLField(blank=True, default='', null=True, verbose_name='توییتر'),
        ),
    ]
