# Generated by Django 2.1.7 on 2019-05-14 05:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('royan_admin', '0002_royantucagene'),
    ]

    operations = [
        migrations.AlterField(
            model_name='royantucagene',
            name='fax',
            field=models.IntegerField(blank=True, null=True, verbose_name='فکس'),
        ),
    ]
