from django.db import models


class Category(models.Model):
    name = models.CharField(verbose_name="نام", max_length=100)
    description = models.TextField(verbose_name="توضیحات", max_length=2000)
    is_active = models.BooleanField(default=True)


class Product(models.Model):
    name = models.CharField(verbose_name="نام", max_length=100)
    description = models.TextField(verbose_name="توضیحات", max_length=2000)
    price = models.IntegerField(verbose_name="قیمت", default=0)
    is_available = models.BooleanField(verbose_name="موجود", default=True)
    count = models.IntegerField(verbose_name="تعداد", default=0)
    image = models.ImageField(default='')
    category = models.ForeignKey(Category, default=None, on_delete="Restrict")
    is_active = models.BooleanField(default=True)
