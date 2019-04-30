from django.db import models
from django_jalali.db import models as jmodels

from apps.registration.models import Customer
from apps.service.models import Service


def user_directory_path(instance, filename):
    return 'orders/user_{0}/service_{1}/{2}'.format(instance.customer.username, instance.service.id, filename)


class OrderService(models.Model):
    name = models.CharField(max_length=40, default="", verbose_name="نام فاکتور شونده", blank=True)
    customer = models.ForeignKey(Customer, on_delete="Cascade", verbose_name="سفارش دهنده")
    service = models.ForeignKey(Service, on_delete="DoNothing", verbose_name="سرویس")
    file = models.FileField(verbose_name="فایل", upload_to=user_directory_path, blank=True)
    is_finished = models.BooleanField(default=False, verbose_name="وضعیت سفارش")
    code = models.CharField(default="PR", blank=True, max_length=40, verbose_name="کد")
    date = jmodels.jDateField(verbose_name="تاریخ", blank=True, null=True)
    invoice = models.BooleanField(default=False, verbose_name="وضعیت پیش فاکتور")
    received = models.BooleanField(default=False, verbose_name="وضعیت تحویل")
    payed = models.BooleanField(default=False, verbose_name="وضعیت پرداخت")
    payment = models.IntegerField(default=0, verbose_name="مبلغ")
