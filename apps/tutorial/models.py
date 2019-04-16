from django.db import models


class Tutorial(models.Model):
    name = models.CharField(max_length=30, verbose_name="نام توتوریال")
    description = models.TextField(max_length=1000, verbose_name="توضیحات")


class Links(models.Model):
    title = models.CharField(max_length=30, verbose_name="عنوان بخش")
    description = models.TextField(max_length=1000, verbose_name="توضیحات")
    link = models.URLField(max_length=128,
                           blank=True, verbose_name="لینک")
    tutorial = models.ForeignKey(Tutorial, verbose_name="توتوریال", default=None, on_delete="Restrict")
    rank = models.IntegerField(verbose_name="مکان نسبی", default=0)
