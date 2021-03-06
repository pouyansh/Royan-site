# Generated by Django 2.1.7 on 2019-05-07 08:27

from django.db import migrations, models
import django_jalali.db.models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('product', '0007_auto_20190411_1648'),
        ('registration', '0006_customer_is_person'),
    ]

    operations = [
        migrations.CreateModel(
            name='OrderProduct',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('price', models.IntegerField(verbose_name='قیمت')),
                ('description', models.TextField(max_length=1000, verbose_name='توضیحات اضافه')),
                ('received', models.BooleanField(default=False, verbose_name='آیا تحویل داده شده است؟')),
                ('invoice', models.BooleanField(default=False, verbose_name='آیا پیش فاکتور ارسال شده است؟')),
                ('payed', models.BooleanField(default=False, verbose_name='آیا پرداخت شده است؟')),
                ('date', django_jalali.db.models.jDateField(blank=True, null=True, verbose_name='تاریخ')),
                ('customer', models.ForeignKey(on_delete='Cascade', to='registration.Customer', verbose_name='مشتری')),
                ('product', models.ForeignKey(on_delete='Cascade', to='product.Product', verbose_name='کالا')),
            ],
        ),
    ]
