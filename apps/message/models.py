from django.db import models
from django_jalali.db import models as jmodels

from apps.registration.models import Customer


class Message(models.Model):
    customer = models.ForeignKey(Customer, related_name="customer", on_delete="Cascade", verbose_name="مشتری")
    is_sender = models.BooleanField(verbose_name="مشتری پیام را فرستاده", default=True)
    title = models.CharField(max_length=100, verbose_name="عنوان")
    text = models.TextField(max_length=2000, verbose_name="متن")
    date = jmodels.jDateTimeField(verbose_name="تاریخ", auto_now=True)
    is_opened = models.BooleanField(verbose_name="وضعیت مشاهده", default=False)
    parent = models.ForeignKey("Message", related_name="parent_message", default=None, blank=True,
                               null=True, on_delete="DoNothing")
