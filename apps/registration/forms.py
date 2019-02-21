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
	first_name = forms.CharField(max_length=30, required=False, help_text='Optional.')
	last_name = forms.CharField(max_length=30, required=False, help_text='Optional.')
	email = forms.EmailField(max_length=254, help_text='Required. Inform a valid email address.')
	code = forms.CharField(max_length=20, min_length=10, required=False)
	state = forms.CharField(label='استان')
	city = forms.CharField(label='شهر')
	district = forms.CharField(label="محله")

	def __init__(self, *args, **kwargs):
		if 'url' in kwargs:
			self.url = kwargs.pop('url')
		else:
			self.url = '127.0.0.0.1:8000/'

		super(UserCreationForm, self).__init__(*args, **kwargs)
		self.fields['email'].label = "ایمیل"
		self.fields['code'].label = "کد معرفی"
		self.fields['username'].label = "نام کاربری"
		self.fields['first_name'].label = "نام"
		self.fields['last_name'].label = "نام خانوادگی"
		self.fields['password1'].label = "رمز عبور"
		self.fields['password2'].label = "تکرار رمز عبور"

	class Meta:
		model = Customer
		fields = (
			'username', 'first_name', 'last_name', 'email', 'password1', 'password2',)

	def clean_code(self):
		code = self.cleaned_data.get('code')
		print(' i am cleaning code! ')
		if code:
			try:
				username = code.replace('INVITEBY', '')
				customer = Customer.objects.get(username=username)
				return username
			except:
				raise forms.ValidationError("کد معرفی نامعتبر است.")


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
