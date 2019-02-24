from math import ceil

from django import forms
from django.core.mail import send_mail
from django.forms import ModelForm
from django.contrib.auth.forms import UserCreationForm, SetPasswordForm
from django.contrib.auth.forms import PasswordChangeForm as DjangoPasswordChangeForm

from apps.registration.models import Customer
from backend_settings import settings


class ChangePasswordForm(DjangoPasswordChangeForm):
    def __init__(self, user, *args, **kwargs):
        super().__init__(user, *args, **kwargs)
        self.fields['old_password'].label = "رمز عبور"
        self.fields['new_password1'].label = "رمز عبور جدید"
        self.fields['new_password2'].label = "تکرار رمز عبور جدید"


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

    def __init__(self, *args, **kwargs):
        if 'url' in kwargs:
            self.url = kwargs.pop('url')
        else:
            self.url = '127.0.0.0.1:8000/'

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

    class Meta:
        model = Customer
        fields = (
            'first_name', 'last_name', 'organization_name', 'national_id', 'submit_id',
            'economic_id', 'post', 'education', 'org', 'email', 'phone_number', 'cellphone_number', 'fax', 'address',
            'username', 'password1', 'password2',)


class EditProfileForm(ModelForm):
    state = forms.CharField(label='استان')
    city = forms.CharField(label='شهر')
    district = forms.CharField(label="محله")

    class Meta:
        model = Customer
        fields = ('first_name', 'last_name')


class ForgetPassForm(forms.Form):
    username = forms.CharField(max_length=20, required=True, label="نام کاربری")

    class Meta:
        model = Customer
        fields = 'username'

    def send_email(self):
        username = self.cleaned_data['username']
        user = Customer.objects.get(username=username)
        send_mail(
            'بازیابی رمز عبور',
            'لطفا برروی لینک زیر کلیک نمایید:\n'
            '127.0.0.1:8000/reset_password/' + Hash.dohash(user.email + '`' + user.username),
            settings.EMAIL_HOST_USER,
            [user.email],
            fail_silently=False,
        )


class ResetPasswordForm(SetPasswordForm):
    def __init__(self, user, *args, **kwargs):
        super().__init__(user, *args, **kwargs)
        self.fields['new_password1'].label = "رمز عبور جدید"
        self.fields['new_password2'].label = "تکرار رمز عبور جدید"


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
