# Generated by Django 2.1.7 on 2019-03-18 01:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('index', '0004_news_date'),
    ]

    operations = [
        migrations.AlterField(
            model_name='news',
            name='description',
            field=models.TextField(default='', max_length=2000, verbose_name='متن خبر (فارسی)'),
        ),
        migrations.AlterField(
            model_name='news',
            name='english_description',
            field=models.TextField(blank=True, default='', max_length=2000, verbose_name='متن خبر (انگلیسی)'),
        ),
    ]
