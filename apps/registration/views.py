from django.core.mail import send_mail
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, get_object_or_404

from django.http import HttpResponseRedirect
from django.utils.translation import gettext_lazy as _
from django.views.generic import CreateView, UpdateView, FormView, TemplateView
from django.contrib.auth.views import LoginView
from django.contrib.auth.views import PasswordChangeView as DjangoPasswordChangeView

from apps.registration.forms import *
from django.contrib.auth import logout

from apps.registration.models import *


class Dashboard(TemplateView):
	template_name = 'dashboard/dashboard.html'


class ChangePassword(DjangoPasswordChangeView):
	form_class = ChangePasswordForm
	success_url = reverse_lazy('dashboard:dashboard')
	template_name = 'registeration/change_password.html'
	title = _('تغییر رمز عبور')


class Login(LoginView):
	template_name = 'registeration/login.html'
	redirect_authenticated_user = True


class Register(CreateView):
	form_class = SignUpForm
	template_name = 'registeration/register.html'

	def success_response(self, request, message, **kwargs):
		context = self.get_context_data(**kwargs)
		context['message'] = message
		context['form'] = SignUpForm
		return render(request, self.template_name, context)


class EditProfile(LoginRequiredMixin, UpdateView):
	form_class = EditProfileForm

	template_name = 'registeration/edit_profile.html'
	success_url = reverse_lazy('dashboard:dashboard')

	def get_object(self, queryset=None):
		return Customer.objects.get(username=self.request.user.username)

	def form_valid(self, form):
		user = Customer.objects.get(username=self.request.user.username)
		form.instance.user = user

		return super().form_valid(form)


class ResetPassword(FormView):
	model = Customer
	form_class = None
	template_name = 'registeration/reset_password.html'
	success_url = '/logout'

	def __init__(self, user, **kwargs):
		super().__init__(**kwargs)
		self.form_class = ResetPasswordForm(user)


def error(request, param):
	pass


class ForgetPassword(FormView):
	template_name = 'registeration/forget_password.html'
	form_class = ForgetPassForm
	success_url = reverse_lazy('registeration:login')

	def form_valid(self, form):
		try:
			Customer.objects.get(username=form.instance.username)
		except:
			return error(self.request, 'نام کاربری مورد نظر در سامانه ثبت نشده است.')
		form.send_email()
		return super().form_valid(form)


def create_referral_code(username):
	return f'INVITEBY{username}'


class GetReferralCode(LoginRequiredMixin, TemplateView):
	template_name = 'registeration/referral_code.html'

	def get_context_data(self, **kwargs):
		context = super().get_context_data(**kwargs)

		context['code'] = create_referral_code(self.request.user.username)
		context['amount'] = 10000
		return context


def login_success(request):
	print(request.user.is_authenticated)
	if not request.user.is_authenticated:
		return HttpResponseRedirect(reverse_lazy('registeration:login'))
	try:
		user = Customer.objects.get(username=request.user.username)
		if user.email_verified:
			return HttpResponseRedirect(reverse_lazy('dashboard:dashboard'))
		logout(request)
		return error(request, "لطفا برای ورود به سایت ابتدا بر روی لینک ارسال شده به آدرس ایمیل خود کلیک کنید.")
	except:
		return HttpResponseRedirect('/admin/')


def log_out(request):
	logout(request)
	return HttpResponseRedirect(reverse_lazy('registeration:login'))


def verify_email(request, username):
	logout(request)
	try:
		splited = Hash.unhash(username).split('`')
		user_name = splited[0]
		email = splited[1]
		user = Customer.objects.get(username=user_name, email=email)
		if user.email_verified:
			return error(request, "ثبت نام شما قبلا تایید شده است.")
	except:
		return error(request, "توکن دریافت شده نامعتبر است.")
	user.email_verified = True
	user.save()
	return HttpResponseRedirect(reverse_lazy('registeration:login'))


def reset_password(request, username):
	template_name = 'registeration/reset_password.html'
	context = {}

	splited = Hash.unhash(username).split('`')
	user_name = splited[1]
	email = splited[0]
	reset = get_object_or_404(Customer, username=user_name, email=email)
	form = SetPasswordForm(user=reset, data=request.POST or None)

	if form.is_valid():
		form.save()
		context['success'] = True

	context['form'] = form
	if request.POST:
		return HttpResponseRedirect(reverse_lazy('registeration:login'))
	return render(request, template_name, context)
