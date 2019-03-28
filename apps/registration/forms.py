from math import ceil

from django import forms
from django.contrib.auth.forms import UserCreationForm
from apps.registration.models import *


class SignUpOrganization(UserCreationForm):
    def __init__(self, *args, **kwargs):
        super(SignUpOrganization, self).__init__(*args, **kwargs)
        self.fields['email'].label = "ایمیل"
        self.fields['email'].required = True
        self.fields['username'].label = "نام کاربری"
        self.fields['password1'].label = "رمز عبور"
        self.fields['password2'].label = "تکرار رمز عبور"

    class Meta:
        model = Organization
        fields = (
            'organization_name', 'post', 'submit_id', 'economic_id', 'email', 'phone_number', 'fax', 'address',
            'username', 'password1', 'password2')

    def clean_username(self):
        username = self.cleaned_data['username']
        user_exists = Customer.objects.filter(username=username)
        if user_exists:
            raise forms.ValidationError("نام کاربری تکراری است.")
        return username

    def clean_email(self):
        email = self.cleaned_data['email']
        user_exists = Customer.objects.filter(email=email)
        if len(user_exists) > 0:
            raise forms.ValidationError("ایمیل وارد شده تکراری است.")
        return email

    def clean_organization_name(self):
        org_name = self.cleaned_data['organization_name']
        user_exists = Organization.objects.filter(organization_name=org_name)
        if len(user_exists) > 0:
            raise forms.ValidationError("نام شرکت تکراری است.")
        return org_name

    def clean_economic_id(self):
        eid = self.cleaned_data['economic_id']
        user_exists = Organization.objects.filter(economic_id=eid)
        if user_exists:
            raise forms.ValidationError("شماره اقتصادی تکراری است.")
        return eid

    def clean_submit_id(self):
        sid = self.cleaned_data['submit_id']
        user_exists = Organization.objects.filter(submit_id=sid)
        if user_exists:
            raise forms.ValidationError("شماره ثبت تکراری است.")
        return sid


class SignUpPerson(UserCreationForm):
    def __init__(self, *args, **kwargs):
        super(SignUpPerson, self).__init__(*args, **kwargs)
        self.fields['email'].label = "ایمیل"
        self.fields['email'].required = True
        self.fields['username'].label = "نام کاربری"
        self.fields['first_name'].label = "نام"
        self.fields['first_name'].required = True
        self.fields['last_name'].label = "نام خانوادگی"
        self.fields['last_name'].required = True
        self.fields['password1'].label = "رمز عبور"
        self.fields['password2'].label = "تکرار رمز عبور"

    class Meta:
        model = Person
        fields = (
            'first_name', 'last_name', 'national_id', 'education', 'org',
            'email', 'phone_number', 'cellphone_number', 'fax', 'address',
            'username', 'password1', 'password2')

    def clean_username(self):
        username = self.cleaned_data['username']
        user_exists = Customer.objects.filter(username=username)
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
        user_exists = Person.objects.filter(national_id=nid)
        if user_exists:
            raise forms.ValidationError("کد ملی تکراری است.")
        if len(str(nid)) != 10:
            raise forms.ValidationError("کد ملی باید 10 رقمی باشد.")
        print(nid)
        return nid


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
