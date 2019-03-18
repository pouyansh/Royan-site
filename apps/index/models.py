from django.db import models


class News(models.Model):
    title = models.CharField(max_length=150)
    image = models.ImageField()
    description = models.CharField(max_length=1000)
