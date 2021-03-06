# Generated by Django 2.1.7 on 2019-07-28 11:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('registration', '0007_auto_20190604_0328'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customer',
            name='address',
            field=models.CharField(max_length=1500, verbose_name='آدرس'),
        ),
        migrations.AlterField(
            model_name='organization',
            name='organization_name',
            field=models.CharField(max_length=300, verbose_name='نام شرکت'),
        ),
        migrations.AlterField(
            model_name='organization',
            name='post',
            field=models.CharField(max_length=200, verbose_name='سمت'),
        ),
        migrations.AlterField(
            model_name='person',
            name='org',
            field=models.CharField(max_length=300, verbose_name='موسسه/آموزشگاه/سازمان'),
        ),
    ]
