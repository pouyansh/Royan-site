from django.contrib.auth.views import LoginView, LogoutView
from django.urls import reverse_lazy
from django.views.generic import TemplateView, CreateView

from apps.product.models import Category
from apps.registration.forms import *
from apps.service.models import Service, Field


class Login(LoginView):
    model = User
    template_name = 'registration/login.html'
    success_url = reverse_lazy('index:index')


class LoginSuccess(TemplateView):
    template_name = 'registration/login_success.html'


class Logout(LogoutView):
    model = User


class RegisterPerson(CreateView):
    model = Person
    form_class = SignUpPerson
    template_name = 'registration/register_user.html'
    success_url = reverse_lazy('index:index')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['product_categories'] = Category.objects.all()
        context['services'] = Service.objects.all()
        context['service_fields'] = Field.objects.all()
        return context


class RegisterOrganization(CreateView):
    model = Organization
    form_class = SignUpOrganization
    template_name = 'registration/register_user.html'
    success_url = reverse_lazy('index:index')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['product_categories'] = Category.objects.all()
        context['services'] = Service.objects.all()
        context['service_fields'] = Field.objects.all()
        return context
