from django.db import models


class News(models.Model):
    title = models.CharField(max_length=450, default='', verbose_name="عنوان خبر (فارسی)")
    image = models.ImageField()
    summary = models.CharField(max_length=1500, default='', verbose_name="خلاصه خبر (فارسی)")
    description = models.TextField(max_length=4000, default='', verbose_name="متن خبر (فارسی)")
    english_title = models.CharField(max_length=450, default='', blank=True, verbose_name="عنوان خبر (انگلیسی)")
    english_summary = models.CharField(max_length=1500, default='', blank=True, verbose_name="خلاصه خبر (انگلیسی)")
    english_description = models.TextField(max_length=4000, default='', blank=True, verbose_name="متن خبر (انگلیسی)")
    date = models.DateTimeField(verbose_name="تاریخ", auto_now_add=True, blank=True)
    file = models.FileField(verbose_name="فایل", blank=True, default=None, null=True, name="file")
