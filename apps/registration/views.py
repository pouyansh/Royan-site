from django.contrib.auth.views import LoginView, LogoutView
from django.core.mail import send_mail
from django.urls import reverse_lazy
from django.views.generic import TemplateView, CreateView, FormView

from apps.product.models import Category
from apps.registration.forms import *
from apps.service.models import Service, Field


class Login(LoginView):
    model = User
    template_name = 'registration/login.html'
    success_url = reverse_lazy('registration:login_success')


class LoginSuccess(TemplateView):
    template_name = 'registration/login_success.html'


class Logout(LogoutView):
    model = User


class RegisterPerson(CreateView):
    model = Person
    form_class = SignUpPerson
    template_name = 'registration/register_user.html'
    success_url = reverse_lazy('registration:registered')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['product_categories'] = Category.objects.all()
        context['services'] = Service.objects.all()
        context['service_fields'] = Field.objects.all()
        return context

    def form_valid(self, form):
        person = form.save(commit=False)
        person.is_active = False
        person.save()
        email = form.cleaned_data['email']
        username = form.cleaned_data['username']
        hashed_data = '127.0.0.1:8000/verify_email/' + Hash.code(username + '#' + email)
        send_mail('تایید ایمیل',
                  'بسیار سپاس‌گزاریم که در سایت شرکت رویان توکاژن ثبت نام کردید. ' +
                  'لطفا برای تایید ایمیل خود، بر روی لینک زیر کلیک نمایید.\n' +
                  hashed_data + '/', 'tucagenesite@gmail.com', [email])
        return super(RegisterPerson, self).form_valid(form)


class RegisterOrganization(CreateView):
    model = Organization
    form_class = SignUpOrganization
    template_name = 'registration/register_user.html'
    success_url = reverse_lazy('registration:registered')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['product_categories'] = Category.objects.all()
        context['services'] = Service.objects.all()
        context['service_fields'] = Field.objects.all()
        return context

    def form_valid(self, form):
        organization = form.save(commit=False)
        organization.first_name = organization.post
        organization.last_name = organization.organization_name
        organization.is_active = False
        organization.save()
        email = form.cleaned_data['email']
        username = form.cleaned_data['username']
        hashed_data = '127.0.0.1:8000/verify_email/' + Hash.code(username + '#' + email)
        send_mail('تایید ایمیل',
                  'بسیار سپاس‌گزاریم که در سایت شرکت رویان توکاژن ثبت نام کردید. ' +
                  'لطفا برای تایید ایمیل خود، بر روی لینک زیر کلیک نمایید.\n' +
                  hashed_data + '/', 'tucagenesite@gmail.com', [email])
        return super(RegisterOrganization, self).form_valid(form)


class RegisteredSuccessfully(TemplateView):
    template_name = 'temporary/show_text.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['product_categories'] = Category.objects.all()
        context['services'] = Service.objects.all()
        context['service_fields'] = Field.objects.all()
        context['text'] = "اطلاعات شما با موفقیت ثبت شد و ایمیلی برای شما ارسال شد." + \
                          " لطفا به آدرس ایمیل خود بروید و برروی لینک ارسال شده کلیک نمایید تا حساب کاربری شما فعال شود"
        return context


class VerifyEmail(FormView):
    template_name = 'registration/verify_email.html'
    form_class = VerifyEmailForm
    success_url = reverse_lazy('registration:verified')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['product_categories'] = Category.objects.all()
        context['services'] = Service.objects.all()
        context['service_fields'] = Field.objects.all()
        return context

    def form_valid(self, form):
        username = form.cleaned_data['username']
        email = form.cleaned_data['email']
        hashed = self.kwargs['keyword']
        decoded = Hash.decode(hashed)
        if decoded == username + "#" + email:
            customer = Customer.objects.get(username=username)
            customer.is_active = True
            customer.save()
        else:
            self.success_url = reverse_lazy('registration:not_verified')
        return super(VerifyEmail, self).form_valid(form)


class VerifiedSuccessfully(TemplateView):
    template_name = 'temporary/show_text.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['product_categories'] = Category.objects.all()
        context['services'] = Service.objects.all()
        context['service_fields'] = Field.objects.all()
        context['text'] = "حساب کاربری شما با موفقیت فعال شد"
        return context


class VerifiedNotSuccessfully(TemplateView):
    template_name = 'temporary/show_text.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['product_categories'] = Category.objects.all()
        context['services'] = Service.objects.all()
        context['service_fields'] = Field.objects.all()
        context['text'] = "متاسفانه اطلاعات وارد شده با لینک مربوط به تایید همخوانی ندارد"
        return context


class Hash:
    @staticmethod
    def code(name):
        sums = [0 for _ in range(ceil(len(name) / 4))]
        for j in range(ceil(len(name) / 4)):
            for i in range(4):
                if 4 * j + i < len(name):
                    sums[j] = sums[j] * 256 + ord(name[4 * j + i])
        result = ''
        for j in range(ceil(len(name) / 4)):
            current_sum = sums[j]
            while current_sum > 25:
                a = current_sum % 26
                current_sum = (current_sum - a) / 26
                result = chr(int(97 + a)) + result
            result = chr(int(65 + current_sum)) + result
        return result

    @staticmethod
    def decode(hashed):
        i = 0
        decoded = ''
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
                decoded = chr(int(a)) + decoded
            decoded = chr(int(sum_result)) + decoded
        return decoded
