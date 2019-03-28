from django.db import models


class Field(models.Model):
    name = models.CharField(max_length=30)
    description = models.TextField(max_length=1000)


class Service(models.Model):
    name = models.CharField(max_length=30)
    description = models.TextField(max_length=2000)
    field = models.ForeignKey(Field, on_delete="Restrict")
