from django.contrib.auth.views import LoginView, LogoutView
from django.urls import reverse_lazy
from django.views.generic import TemplateView, FormView, CreateView

from apps.product.models import Category
from apps.registration.forms import *


class Login(LoginView):
    model = User
    template_name = 'registration/login.html'
    success_url = reverse_lazy('index:index')


class LoginSuccess(TemplateView):
    template_name = 'registration/login_success.html'


class Logout(LogoutView):
    model = User


class RegisterUser(FormView):
    form_class = SignUpOrganization
    template_name = 'registration/register.html'
    success_url = 'index:index'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['product_categories'] = Category.objects.all()
        return context

    def form_valid(self, form):
        user_type = form.cleaned_data['type']
        print(user_type)
        return super(RegisterUser, self).form_valid(form)


class RegisterPerson(CreateView):
    model = Person
    form_class = SignUpPerson
    template_name = 'registration/register_user.html'
    success_url = reverse_lazy('index:index')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['product_categories'] = Category.objects.all()
        return context

    def form_valid(self, form):
        username = form.cleaned_data['username']
        print(username)
        return super(RegisterPerson, self).form_valid(form)


class RegisterOrganization(CreateView):
    model = Organization
    form_class = SignUpOrganization
    template_name = 'registration/register_user.html'
    success_url = reverse_lazy('index:index')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['product_categories'] = Category.objects.all()
        return context

    def form_valid(self, form):
        username = form.cleaned_data['username']
        print(username)
        return super(RegisterOrganization, self).form_valid(form)
