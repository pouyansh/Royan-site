# Generated by Django 2.1.7 on 2019-07-28 11:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('news', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='news',
            name='description',
            field=models.TextField(default='', max_length=4000, verbose_name='متن خبر (فارسی)'),
        ),
        migrations.AlterField(
            model_name='news',
            name='english_description',
            field=models.TextField(blank=True, default='', max_length=4000, verbose_name='متن خبر (انگلیسی)'),
        ),
        migrations.AlterField(
            model_name='news',
            name='english_summary',
            field=models.CharField(blank=True, default='', max_length=1500, verbose_name='خلاصه خبر (انگلیسی)'),
        ),
        migrations.AlterField(
            model_name='news',
            name='english_title',
            field=models.CharField(blank=True, default='', max_length=450, verbose_name='عنوان خبر (انگلیسی)'),
        ),
        migrations.AlterField(
            model_name='news',
            name='summary',
            field=models.CharField(default='', max_length=1500, verbose_name='خلاصه خبر (فارسی)'),
        ),
        migrations.AlterField(
            model_name='news',
            name='title',
            field=models.CharField(default='', max_length=450, verbose_name='عنوان خبر (فارسی)'),
        ),
    ]
