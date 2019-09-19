from django.contrib.auth.models import User
from django.db import models


class Customer(User):
    phone_number = models.IntegerField(verbose_name="شماره تلفن ثابت")
    fax = models.IntegerField(null=True, verbose_name="فکس")
    address = models.CharField(max_length=1500, verbose_name='آدرس')
    email_verified = models.BooleanField(default=False, verbose_name="ایمیل تایید شده است")
    is_person = models.BooleanField(default=False)
    is_blocked = models.BooleanField(default=False)

    def get_full_name(self):
        return self.first_name + " " + self.last_name


class Organization(Customer):
    organization_name = models.CharField(max_length=300, verbose_name="نام شرکت")
    post = models.CharField(max_length=200, verbose_name="سمت")
    submit_id = models.IntegerField(verbose_name="شماره ثبت")
    economic_id = models.IntegerField(verbose_name="شماره اقتصادی")

    def get_full_name(self):
        return str(self.post) + " " + str(self.organization_name)


class Person(Customer):
    national_id = models.CharField(max_length=10, verbose_name="کد ملی")
    education = models.CharField(max_length=100, verbose_name="تحصیلات", null=True)
    org = models.CharField(max_length=300, verbose_name="موسسه/آموزشگاه/سازمان")
    cellphone_number = models.BigIntegerField(verbose_name="شماره تلفن همراه")
