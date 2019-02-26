from math import ceil

from django import forms
from django.core.mail import send_mail
from django.forms import ModelForm
from django.contrib.auth.forms import UserCreationForm, SetPasswordForm
from django.contrib.auth.forms import PasswordChangeForm as DjangoPasswordChangeForm
from django.shortcuts import get_object_or_404

from apps.registration.models import *
from backend_settings import settings


class SignUpForm(UserCreationForm):
    organization_name = forms.CharField(max_length=100)
    post = forms.CharField(max_length=100)
    submit_id = forms.IntegerField()
    economic_id = forms.IntegerField()
    national_id = forms.IntegerField()
    education = forms.CharField(max_length=100)
    org = forms.CharField(max_length=100)
    cellphone_number = forms.IntegerField()
    fax = forms.IntegerField(required=False)
    type = forms.ChoiceField(choices={(1, "حقیقی"), (2, "حقوقی")})

    def __init__(self, *args, **kwargs):
        super(UserCreationForm, self).__init__(*args, **kwargs)
        self.fields['email'].label = "ایمیل"
        self.fields['email'].required = True
        self.fields['username'].label = "نام کاربری"
        self.fields['first_name'].label = "نام"
        self.fields['first_name'].required = True
        self.fields['last_name'].label = "نام خانوادگی"
        self.fields['last_name'].required = True
        self.fields['password1'].label = "رمز عبور"
        self.fields['password2'].label = "تکرار رمز عبور"
        self.fields['national_id'].label = "کد ملی"
        self.fields['economic_id'].label = "شماره اقتصادی"
        self.fields['submit_id'].label = "شماره ثبت"
        self.fields['org'].label = "موسسه/آموزشگاه/سازمان"
        self.fields['organization_name'].label = "نام شرکت"
        self.fields['post'].label = "سمت"
        self.fields['education'].label = "تحصیلات"
        self.fields['phone_number'].label = "تلفن ثابت"
        self.fields['fax'].label = "فکس"
        self.fields['address'].label = "آدرس"
        self.fields['cellphone_number'].label = "تلفن همراه"
        self.fields['type'].label = "نوع حساب کاربری"

    class Meta:
        model = Customer
        fields = (
            'type', 'first_name', 'last_name', 'organization_name', 'national_id', 'submit_id',
            'economic_id', 'post', 'education', 'org', 'email', 'phone_number', 'cellphone_number', 'fax', 'address',
            'username', 'password1', 'password2')

    def clean_username(self):
        username = self.cleaned_data['username']
        try:
            user_exists = Customer.objects.get(username=username)
        except Customer.DoesNotExist:
            user_exists = None
        if user_exists:
            raise forms.ValidationError("نام کاربری تکراری است.")
        return username

    def clean_email(self):
        email = self.cleaned_data['email']
        user_exists = Customer.objects.filter(email=email)
        if len(user_exists) > 0:
            raise forms.ValidationError("ایمیل وارد شده تکراری است.")
        return email

    def clean_national_id(self):
        nid = self.cleaned_data['national_id']
        customer_type = self.cleaned_data['type']
        if customer_type == 1:
            user_exists = get_object_or_404(Person, national_id=nid)
            if user_exists:
                raise forms.ValidationError("کد ملی تکراری است.")
        if len(str(nid)) != 10:
            raise forms.ValidationError("کد ملی باید 10 رقمی باشد.")
        return nid

    def clean_organization_name(self):
        org_name = self.cleaned_data['orgaization_name']
        user_exists = Organization.objects.filter(organization_name=org_name)
        if len(user_exists) > 0:
            raise forms.ValidationError("نام شرکت تکراری است.")
        return org_name


class Hash:
    @staticmethod
    def dohash(name):
        sums = [0 for _ in range(ceil(len(name) / 4))]
        for j in range(ceil(len(name) / 4)):
            for i in range(4):
                if 4 * j + i < len(name):
                    sums[j] = sums[j] * 256 + ord(name[4 * j + i])
        res = ''
        for j in range(ceil(len(name) / 4)):
            current_sum = sums[j]
            while current_sum > 25:
                a = current_sum % 26
                current_sum = (current_sum - a) / 26
                res = chr(int(97 + a)) + res
            res = chr(int(65 + current_sum)) + res
        return res

    @staticmethod
    def unhash(hashed):
        i = 0
        dehashed = ''
        while i < len(hashed):
            sum_result = ord(hashed[i]) - 65
            i += 1
            while i < len(hashed) and ord(hashed[i]) >= 97:
                a = ord(hashed[i]) - 97
                sum_result = sum_result * 26 + a
                i += 1
            while sum_result > 255:
                a = sum_result % 256
                sum_result = (sum_result - a) / 256
                dehashed = chr(int(a)) + dehashed
            dehashed = chr(int(sum_result)) + dehashed
        return dehashed
