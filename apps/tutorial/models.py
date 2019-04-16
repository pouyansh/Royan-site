from django.db import models


class Tutorial(models.Model):
    name = models.CharField(max_length=30, verbose_name="نام توتوریال")
    description = models.TextField(max_length=1000, verbose_name="توضیحات")


class Paper(models.Model):
    title = models.CharField(max_length=200, verbose_name="")
    summary = models.TextField(max_length=1000, verbose_name="")
    tutorial = models.ForeignKey(Tutorial, on_delete="Restrict", verbose_name="")
    link = models.FileField(verbose_name="", name="paper", upload_to="", storage="")
