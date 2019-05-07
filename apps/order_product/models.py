from django.db import models
from django_jalali.db import models as jmodels

from apps.product.models import Product
from apps.registration.models import Customer


class OrderProduct(models.Model):
    customer = models.ForeignKey(Customer, verbose_name="مشتری", on_delete="Cascade")
    product = models.ForeignKey(Product, verbose_name="کالا", on_delete="Cascade")
    price = models.IntegerField(verbose_name="قیمت", default=0)
    description = models.TextField(max_length=1000, default="", verbose_name="توضیحات اضافه")
    received = models.BooleanField(default=False, verbose_name="آیا تحویل داده شده است؟")
    invoice = models.BooleanField(default=False, verbose_name="آیا پیش فاکتور ارسال شده است؟")
    payed = models.BooleanField(default=False, verbose_name="آیا پرداخت شده است؟")
    date = jmodels.jDateField(verbose_name="تاریخ", blank=True, null=True)
    is_finished = models.BooleanField(default=False, verbose_name="آیا به اتمام رسیده است؟")
