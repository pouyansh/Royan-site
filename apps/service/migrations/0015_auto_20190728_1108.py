# Generated by Django 2.1.7 on 2019-07-28 11:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('service', '0014_auto_20190720_1219'),
    ]

    operations = [
        migrations.AlterField(
            model_name='field',
            name='description',
            field=models.TextField(max_length=4000, verbose_name='توضیحات'),
        ),
        migrations.AlterField(
            model_name='field',
            name='name',
            field=models.CharField(max_length=150, verbose_name='نام زمینه'),
        ),
        migrations.AlterField(
            model_name='field2',
            name='description',
            field=models.TextField(max_length=4000, verbose_name='توضیحات'),
        ),
        migrations.AlterField(
            model_name='field2',
            name='name',
            field=models.CharField(max_length=150, verbose_name='نام زمینه'),
        ),
        migrations.AlterField(
            model_name='service',
            name='description',
            field=models.TextField(max_length=10000, verbose_name='توضیحات'),
        ),
        migrations.AlterField(
            model_name='service',
            name='name',
            field=models.CharField(max_length=150, verbose_name='نام سرویس'),
        ),
    ]
