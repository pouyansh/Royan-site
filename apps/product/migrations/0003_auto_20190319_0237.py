# Generated by Django 2.1.7 on 2019-03-19 02:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('product', '0002_auto_20190319_0234'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='description',
            field=models.TextField(max_length=2000, verbose_name='توضیحات'),
        ),
    ]
