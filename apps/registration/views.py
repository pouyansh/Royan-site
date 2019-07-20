import random
import string

from django.contrib.auth.views import LoginView, LogoutView, PasswordChangeView
from django.core.mail import send_mail
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.views.generic import TemplateView, CreateView, FormView, UpdateView
from math import ceil

from apps.product.models import Category
from apps.registration.forms import *
from apps.research.models import ResearchArea
from apps.royan_admin.models import RoyanTucagene
from apps.service.models import Service, Field, Field2
from apps.tutorial.models import Tutorial


class Login(LoginView):
    model = User
    template_name = 'registration/login.html'
    success_url = reverse_lazy('registration:login_success')

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect('index:index')
        return super().dispatch(request, *args, **kwargs)


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
        context['RoyanTucagene'] = RoyanTucagene.objects.all()[0]
        context['product_categories'] = Category.objects.filter(is_active=True).order_by('id')
        context['services'] = Service.objects.all().order_by('id')
        context['service_fields'] = Field.objects.all().order_by('id')
        context['research_areas'] = ResearchArea.objects.all().order_by('id')
        context['tutorials'] = Tutorial.objects.all().order_by('id')
        context['title'] = "فرم ثبت نام"
        context['fields2'] = Field2.objects.all().order_by('id')
        return context

    def form_valid(self, form):
        person = form.save(commit=False)
        person.is_active = False
        person.is_person = True
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
        context['RoyanTucagene'] = RoyanTucagene.objects.all()[0]
        context['product_categories'] = Category.objects.filter(is_active=True).order_by('id')
        context['services'] = Service.objects.all().order_by('id')
        context['service_fields'] = Field.objects.all().order_by('id')
        context['research_areas'] = ResearchArea.objects.all().order_by('id')
        context['tutorials'] = Tutorial.objects.all().order_by('id')
        context['title'] = "فرم ثبت نام"
        context['fields2'] = Field2.objects.all().order_by('id')
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
        context['RoyanTucagene'] = RoyanTucagene.objects.all()[0]
        context['product_categories'] = Category.objects.filter(is_active=True).order_by('id')
        context['services'] = Service.objects.all().order_by('id')
        context['service_fields'] = Field.objects.all().order_by('id')
        context['research_areas'] = ResearchArea.objects.all().order_by('id')
        context['tutorials'] = Tutorial.objects.all().order_by('id')
        context['fields2'] = Field2.objects.all().order_by('id')
        context['text'] = "اطلاعات شما با موفقیت ثبت شد و ایمیلی برای شما ارسال شد." + \
                          " لطفا به آدرس ایمیل خود بروید و برروی لینک ارسال شده کلیک نمایید تا حساب کاربری شما فعال شود"
        return context


class VerifyEmail(FormView):
    template_name = 'registration/verify_email.html'
    form_class = VerifyEmailForm
    success_url = reverse_lazy('registration:verified')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['RoyanTucagene'] = RoyanTucagene.objects.all()[0]
        context['product_categories'] = Category.objects.filter(is_active=True).order_by('id')
        context['services'] = Service.objects.all().order_by('id')
        context['service_fields'] = Field.objects.all().order_by('id')
        context['research_areas'] = ResearchArea.objects.all().order_by('id')
        context['tutorials'] = Tutorial.objects.all().order_by('id')
        context['fields2'] = Field2.objects.all().order_by('id')
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
        context['RoyanTucagene'] = RoyanTucagene.objects.all()[0]
        context['product_categories'] = Category.objects.filter(is_active=True).order_by('id')
        context['services'] = Service.objects.all().order_by('id')
        context['service_fields'] = Field.objects.all().order_by('id')
        context['research_areas'] = ResearchArea.objects.all().order_by('id')
        context['tutorials'] = Tutorial.objects.all().order_by('id')
        context['text'] = "حساب کاربری شما با موفقیت فعال شد"
        context['fields2'] = Field2.objects.all().order_by('id')
        return context


class VerifiedNotSuccessfully(TemplateView):
    template_name = 'temporary/show_text.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['RoyanTucagene'] = RoyanTucagene.objects.all()[0]
        context['product_categories'] = Category.objects.filter(is_active=True).order_by('id')
        context['services'] = Service.objects.all().order_by('id')
        context['service_fields'] = Field.objects.all().order_by('id')
        context['research_areas'] = ResearchArea.objects.all().order_by('id')
        context['tutorials'] = Tutorial.objects.all().order_by('id')
        context['text'] = "متاسفانه اطلاعات وارد شده با لینک مربوط به تایید همخوانی ندارد"
        context['fields2'] = Field2.objects.all().order_by('id')
        return context


class UpdateCustomer(UpdateView):
    model = Customer
    form_class = UpdateOrganizationForm
    template_name = 'registration/register_user.html'
    success_url = reverse_lazy('registration:updated')

    def get_object(self, queryset=None):
        organization = Organization.objects.filter(username=self.request.user.username)
        if len(organization) > 0:
            self.form_class = UpdateOrganizationForm
            return organization[0]
        self.form_class = SignUpPerson
        person = Person.objects.filter(username=self.request.user.username)
        return person[0]

    def get_context_data(self, **kwargs):
        context = super(UpdateCustomer, self).get_context_data(**kwargs)
        context['RoyanTucagene'] = RoyanTucagene.objects.all()[0]
        context['product_categories'] = Category.objects.filter(is_active=True).order_by('id')
        context['services'] = Service.objects.all().order_by('id')
        context['service_fields'] = Field.objects.all().order_by('id')
        context['research_areas'] = ResearchArea.objects.all().order_by('id')
        context['tutorials'] = Tutorial.objects.all().order_by('id')
        context['fields2'] = Field2.objects.all().order_by('id')
        return context


class UpdatedSuccessfully(TemplateView):
    template_name = 'temporary/show_text.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['RoyanTucagene'] = RoyanTucagene.objects.all()[0]
        context['product_categories'] = Category.objects.filter(is_active=True).order_by('id')
        context['services'] = Service.objects.all().order_by('id')
        context['service_fields'] = Field.objects.all().order_by('id')
        context['research_areas'] = ResearchArea.objects.all().order_by('id')
        context['tutorials'] = Tutorial.objects.all().order_by('id')
        context['fields2'] = Field2.objects.all().order_by('id')
        context['text'] = "اطلاعات شما با موفقیت ثبت شد و ایمیلی برای شما ارسال شد."
        return context


class ForgetPassword(FormView):
    form_class = ForgetPasswordForm
    template_name = 'registration/forget_password.html'
    success_url = reverse_lazy('registration:forget_password_success')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['RoyanTucagene'] = RoyanTucagene.objects.all()[0]
        context['product_categories'] = Category.objects.filter(is_active=True).order_by('id')
        context['services'] = Service.objects.all().order_by('id')
        context['service_fields'] = Field.objects.all().order_by('id')
        context['research_areas'] = ResearchArea.objects.all().order_by('id')
        context['tutorials'] = Tutorial.objects.all().order_by('id')
        context['fields2'] = Field2.objects.all().order_by('id')
        return context

    def form_valid(self, form):
        customer = Customer.objects.get(email=form.cleaned_data['email'])
        newpass = ''.join(random.choices(string.ascii_uppercase + string.digits, k=10))
        customer.set_password(newpass)
        customer.save()
        send_mail('تغییر رمز عبور',
                  'کاربر گرامی، رمز عبور جدیدی برای حساب کاربری شما ساخته شد که در ادامه مشاهده می‌فرمایید. ' +
                  'خواهشمند است به منظور حفظ مسائل امنیتی، رمز عبور حساب کاربری خود را تغییر دهید.\n' +
                  'username: ' + customer.username + '\n new password: ' + newpass + '\n www.royantucagene.com/login/',
                  'tucagenesite@gmail.com', [customer.email])
        return super(ForgetPassword, self).form_valid(form)


class ForgetPasswordSuccessful(TemplateView):
    template_name = 'temporary/show_text.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['RoyanTucagene'] = RoyanTucagene.objects.all()[0]
        context['product_categories'] = Category.objects.filter(is_active=True).order_by('id')
        context['services'] = Service.objects.all().order_by('id')
        context['service_fields'] = Field.objects.all().order_by('id')
        context['research_areas'] = ResearchArea.objects.all().order_by('id')
        context['tutorials'] = Tutorial.objects.all().order_by('id')
        context['fields2'] = Field2.objects.all().order_by('id')
        context[
            'text'] = "رمز عبور جدید به آدرس ایمیل شما ارسال شد." \
                      " لطفا با استفاده از آن، وارد شوید و رمز عبور خود را تغییر دهید."
        return context


class ChangePassword(PasswordChangeView):
    form_class = PasswordChangeForm
    template_name = 'registration/change_password.html'
    success_url = reverse_lazy('registration:change_password_success')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['RoyanTucagene'] = RoyanTucagene.objects.all()[0]
        context['product_categories'] = Category.objects.filter(is_active=True).order_by('id')
        context['services'] = Service.objects.all().order_by('id')
        context['service_fields'] = Field.objects.all().order_by('id')
        context['research_areas'] = ResearchArea.objects.all().order_by('id')
        context['tutorials'] = Tutorial.objects.all().order_by('id')
        context['fields2'] = Field2.objects.all().order_by('id')
        return context


class ChangePasswordSuccessful(TemplateView):
    template_name = 'temporary/show_text.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['RoyanTucagene'] = RoyanTucagene.objects.all()[0]
        context['product_categories'] = Category.objects.filter(is_active=True).order_by('id')
        context['services'] = Service.objects.all().order_by('id')
        context['service_fields'] = Field.objects.all().order_by('id')
        context['research_areas'] = ResearchArea.objects.all().order_by('id')
        context['tutorials'] = Tutorial.objects.all().order_by('id')
        context['fields2'] = Field2.objects.all().order_by('id')
        context[
            'text'] = "رمز عبور شما با موفقیت تغییر یافت"
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
