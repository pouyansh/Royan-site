from django.db import models


def file_directory_path(instance, filename):
    return 'services_{0}/file.csv'.format(instance.id)


def fields_directory_path(instance, filename):
    return 'services_{0}/fields.csv'.format(instance.id)


class Field(models.Model):
    name = models.CharField(max_length=30, verbose_name='نام زمینه')
    description = models.TextField(max_length=1000, verbose_name='توضیحات')


class Service(models.Model):
    name = models.CharField(max_length=30, verbose_name='نام سرویس')
    description = models.TextField(max_length=2000, verbose_name='توضیحات')
    field = models.ForeignKey(Field, on_delete="Restrict", verbose_name='زمینه‌ی سرویس')
    file = models.FileField(verbose_name="فرم ثبت سفارش", blank=True, null=True, upload_to=file_directory_path)
    has_form = models.BooleanField(default=False, verbose_name="آیا فرم ثبت سفارش دارد؟")
    fields = models.FileField(verbose_name="فیلدهای فرم ثبت نام", default='form.csv', blank=True, null=True,
                              upload_to=fields_directory_path)
