# Generated by Django 2.1.7 on 2019-04-30 06:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('order_service', '0002_auto_20190430_0623'),
    ]

    operations = [
        migrations.AddField(
            model_name='orderservice',
            name='invoice',
            field=models.BooleanField(default=False, verbose_name='وضعیت پیش فاکتور'),
        ),
        migrations.AddField(
            model_name='orderservice',
            name='payed',
            field=models.BooleanField(default=False, verbose_name='وضعیت پرداخت'),
        ),
        migrations.AddField(
            model_name='orderservice',
            name='received',
            field=models.BooleanField(default=False, verbose_name='وضعیت تحویل'),
        ),
        migrations.AlterField(
            model_name='orderservice',
            name='is_finished',
            field=models.BooleanField(default=False, verbose_name='وضعیت سفارش'),
        ),
    ]
