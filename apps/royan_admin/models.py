from django.contrib.auth.models import User
from django.db import models


class RoyanAdmin(User):
    level = models.IntegerField(default=1)


class RoyanTucagene(models.Model):
    logo = models.ImageField(verbose_name="لوگو")
    logo2 = models.ImageField(verbose_name="لوگو۲", blank=True, default=None, null=True)
    summary = models.TextField(max_length=1500, verbose_name="خلاصه (صفحه اصلی)")
    phone_number = models.IntegerField(verbose_name="تلفن")
    address = models.TextField(max_length=3000, verbose_name="آدرس")
    about = models.TextField(max_length=3000, verbose_name="درباره شرکت")
    fax = models.IntegerField(verbose_name="فکس", null=True, blank=True)
    email = models.EmailField(default="", null=True, blank=True)
    instagram = models.URLField(verbose_name="اینستاگرام", default="", null=True, blank=True)
    telegram = models.URLField(verbose_name="تلگرام", default="", null=True, blank=True)
    twitter = models.URLField(verbose_name="توییتر", default="", null=True, blank=True)
    linkedin = models.URLField(verbose_name="لینکداین", default="", null=True, blank=True)
    moto = models.ImageField(verbose_name="شعار", blank=True, default=None, null=True)
