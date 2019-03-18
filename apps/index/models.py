from django.db import models


class News(models.Model):
    title = models.CharField(max_length=150)
    image = models.ImageField()
    summary = models.CharField(max_length=500, default='')
    description = models.CharField(max_length=2000)
