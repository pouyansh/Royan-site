from django.db import models


class Product(models.Model):
    name = models.CharField(verbose_name="نام", max_length=100)
    description = models.CharField(verbose_name="توضیحات", max_length=2000)
    price = models.IntegerField(verbose_name="قیمت")
    is_available = models.BooleanField(verbose_name="موجود")
    count = models.IntegerField(verbose_name="تعداد")
