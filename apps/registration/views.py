from django.shortcuts import render

from django.views.generic import CreateView

from apps.registration.forms import *


class Register(CreateView):
    form_class = SignUpForm
    template_name = 'registration/register.html'
    success_url = 'registration:register'
