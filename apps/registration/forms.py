from math import ceil

from django import forms
from django.core.mail import send_mail
from django.forms import ModelForm
from django.contrib.auth.forms import UserCreationForm, SetPasswordForm
from django.contrib.auth.forms import PasswordChangeForm as DjangoPasswordChangeForm
from django.shortcuts import get_object_or_404

from apps.registration.models import *


class SignUpForm(UserCreationForm):
    organization_name = forms.CharField(max_length=100)
    post = forms.CharField(max_length=100)
    submit_id = forms.IntegerField()
    economic_id = forms.IntegerField()
    national_id = forms.CharField()
    education = forms.CharField(max_length=100)
    org = forms.CharField(max_length=100)
    cellphone_number = forms.IntegerField()
    fax = forms.IntegerField(required=False)
    type = forms.ChoiceField(choices={(2, "حقوقی"), (1, "حقیقی")})

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
        print(nid)
        customer_type = self.cleaned_data['type']
        print("customer_type: ", customer_type)
        if str(customer_type) == "1":
            user_exists = get_object_or_404(Person, national_id=nid)
            if user_exists:
                raise forms.ValidationError("کد ملی تکراری است.")
            if len(str(nid)) != 10:
                raise forms.ValidationError("کد ملی باید 10 رقمی باشد.")
            print(nid)
            return nid
        else:
            return 1

    def clean_organization_name(self):
        org_name = self.cleaned_data['organization_name']
        customer_type = self.cleaned_data['type']
        if customer_type == 1:
            return ''
        user_exists = Organization.objects.filter(organization_name=org_name)
        if len(user_exists) > 0:
            raise forms.ValidationError("نام شرکت تکراری است.")
        return org_name

    def clean_economic_id(self):
        eid = self.cleaned_data['economic_id']
        customer_type = self.cleaned_data['type']
        if customer_type == 2:
            user_exists = get_object_or_404(Organization, economic_id=eid)
            if user_exists:
                raise forms.ValidationError("شماره اقتصادی تکراری است.")
            return eid
        else:
            return 0

    def clean_submit_id(self):
        sid = self.cleaned_data['submit_id']
        customer_type = self.cleaned_data['type']
        if customer_type == 2:
            user_exists = get_object_or_404(Organization, submit_id=sid)
            if user_exists:
                raise forms.ValidationError("شماره ثبت تکراری است.")
            return sid
        else:
            return 0

    def clean_post(self):
        post = self.cleaned_data['post']
        customer_type = self.cleaned_data['type']
        if customer_type == 2:
            user_exists = get_object_or_404(Organization, post=post)
            if user_exists:
                raise forms.ValidationError("شماره ثبت تکراری است.")
            return post
        else:
            return ''

    def clean(self):
        print("hi")
        cleaned_data = super(SignUpForm, self).clean()
        customer_type = cleaned_data['type']
        if customer_type == 1:
            self.instance.organization_name = ""
            self.instance.submit_id = 0
            self.instance.economic_id = 0
            self.instance.post = ""
        else:
            self.instance.national_id = ""
            self.instance.cellphone_number = 0
            self.instance.education = ""
            self.instance.org = ""
        print(self.instance)
        print(cleaned_data)

    def save(self, commit=True):
        user = super(UserCreationForm, self).save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        if commit:
            user.save()
        print("user: ", user)
        return user


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
