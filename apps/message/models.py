from django.contrib.auth.models import User
from django.db import models
from django_jalali.db import models as jmodels


class Message(models.Model):
    Sender = models.ForeignKey(User, related_name="sender", on_delete="Cascade", verbose_name="فرستنده")
    Receiver = models.ForeignKey(User, related_name="receiver", on_delete="Cascade", verbose_name="گیرنده")
    title = models.CharField(max_length=100, verbose_name="عنوان")
    text = models.TextField(max_length=2000, verbose_name="متن")
    date = jmodels.jDateTimeField(verbose_name="تاریخ", auto_now=True)
    is_opened = models.BooleanField(verbose_name="وضعیت مشاهده", default=False)
    parent = models.ForeignKey("Message", related_name="parent_message", verbose_name="", default=None, blank=True,
                               null=True, on_delete="DoNothing")
