# Generated by Django 2.1.7 on 2019-03-19 02:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('product', '0003_auto_20190319_0237'),
    ]

    operations = [
        migrations.AlterField(
            model_name='category',
            name='description',
            field=models.TextField(max_length=2000, verbose_name='توضیحات'),
        ),
    ]
