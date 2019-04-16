from django.db import models


class Tutorial(models.Model):
    name = models.CharField(max_length=30, verbose_name="نام توتوریال")
    description = models.TextField(max_length=1000, verbose_name="توضیحات")

