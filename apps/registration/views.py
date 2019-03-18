from django.contrib.auth.models import User
from django.contrib.auth.views import LoginView
from django.urls import reverse_lazy
from django.views.generic import TemplateView


class Login(LoginView):
    model = User
    template_name = 'registration/login.html'
    success_url = reverse_lazy('index:index')


class LoginSuccess(TemplateView):
    template_name = 'registration/login_success.html'

