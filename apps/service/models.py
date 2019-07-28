from django.db import models


def file_directory_path(instance, filename):
    return 'services/service_{0}/{1}'.format(instance.id, filename)


def fields_directory_path(instance, filename):
    return 'services/service_{0}/fields.csv'.format(instance.id)


class Field(models.Model):
    name = models.CharField(max_length=150, verbose_name='نام زمینه')
    description = models.TextField(max_length=4000, verbose_name='توضیحات')
    image = models.ImageField(verbose_name="عکس", default=None, null=True, blank=True)


class Field2(models.Model):
    name = models.CharField(max_length=150, verbose_name='نام زمینه')
    description = models.TextField(max_length=4000, verbose_name='توضیحات')
    image = models.ImageField(verbose_name="عکس", default=None, null=True, blank=True)
    field = models.ForeignKey(Field, on_delete="Restrict", verbose_name='زمینه‌')


class Service(models.Model):
    name = models.CharField(max_length=150, verbose_name='نام سرویس')
    description = models.TextField(max_length=10000, verbose_name='توضیحات')
    field = models.ForeignKey(Field, on_delete="Restrict", verbose_name='زمینه‌ی سرویس')
    field2 = models.ForeignKey(Field2, on_delete="Restrict", verbose_name='زمینه‌ی دوم سرویس', default=None, null=True,
                               blank=True)
    file = models.FileField(verbose_name="فرم ثبت سفارش", blank=True, null=True, upload_to=file_directory_path)
    has_form = models.BooleanField(default=False, verbose_name="آیا فرم ثبت سفارش دارد؟")
    fields = models.FileField(verbose_name="فیلدهای فرم ثبت نام", blank=True, null=True)
    image = models.ImageField(verbose_name="عکس", default=None, null=True, blank=True)
    logo = models.ImageField(verbose_name="لوگو", default=None, null=True, blank=True)
