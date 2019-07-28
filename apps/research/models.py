from django.db import models


class ResearchArea(models.Model):
    name = models.CharField(max_length=50, verbose_name="نام")
    description = models.TextField(max_length=4000, verbose_name="توضیحات")


class Paper(models.Model):
    title = models.CharField(max_length=400, verbose_name="عنوان مقاله")
    authors = models.CharField(max_length=400, verbose_name="نویسندگان")
    summary = models.TextField(max_length=10000, verbose_name="چکیده")
    research_area = models.ForeignKey(ResearchArea, on_delete="Restrict", verbose_name="زمینه تحقیقاتی")
    paper = models.FileField(verbose_name="مقاله", name="paper")
