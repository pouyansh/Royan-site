from django.db import models

from apps.registration.models import Customer
from apps.service.models import Service


class Order(models.Model):
    customer = models.ForeignKey(Customer, on_delete="Cascade", verbose_name="مشتری")
    service = models.ForeignKey(Service, on_delete="DoNothing", verbose_name="سرویس")
    file = models.FileField(verbose_name="فایل")
    is_finished = models.BooleanField(default=False)
