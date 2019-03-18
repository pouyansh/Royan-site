from django.db import models


class News(models.Model):
    title = models.CharField(max_length=150, default='', verbose_name="عنوان خبر (فارسی)")
    image = models.ImageField()
    summary = models.CharField(max_length=500, default='', verbose_name="خلاصه خبر (فارسی)")
    description = models.CharField(max_length=2000, default='', verbose_name="متن خبر (فارسی)")
    english_title = models.CharField(max_length=150, default='', blank=True, verbose_name="عنوان خبر (انگلیسی)")
    english_summary = models.CharField(max_length=500, default='', blank=True, verbose_name="خلاصه خبر (انگلیسی)")
    english_description = models.CharField(max_length=2000, default='', blank=True, verbose_name="متن خبر (انگلیسی)")
    date = models.DateTimeField(verbose_name="تاریخ", auto_now_add=True, blank=True)
