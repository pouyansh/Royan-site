# Generated by Django 2.1.7 on 2019-07-28 11:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tutorial', '0006_auto_20190416_0938'),
    ]

    operations = [
        migrations.AlterField(
            model_name='links',
            name='description',
            field=models.TextField(max_length=10000, verbose_name='توضیحات'),
        ),
        migrations.AlterField(
            model_name='links',
            name='title',
            field=models.CharField(max_length=150, verbose_name='عنوان بخش'),
        ),
        migrations.AlterField(
            model_name='tutorial',
            name='description',
            field=models.TextField(max_length=4000, verbose_name='توضیحات'),
        ),
        migrations.AlterField(
            model_name='tutorial',
            name='name',
            field=models.CharField(max_length=150, verbose_name='نام توتوریال'),
        ),
    ]
