import json
import urllib

from django.shortcuts import render, redirect

from django.views.generic import CreateView

from apps.registration.forms import *


# class Register(CreateView):
#     form_class = SignUpForm
#     template_name = 'registration/register.html'
#     success_url = 'registration:register'
#
#     def form_valid(self, form):
#         customer = form.save()
#         customer_type = form.type
#         print("type: ", customer_type)
#         if customer_type == 1:
#             national_id = form.national_id
#             education = form.education
#             org = form.org
#             cellphone_number = form.cellphone_number
#             person = Person(national_id=national_id, education=education, org=org, cellphone_number=cellphone_number,
#                             customer=customer)
#             person.save()
from backend_settings import settings


def register(request):

    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():

            ''' Begin reCAPTCHA validation '''
            recaptcha_response = request.POST.get('g-recaptcha-response')
            url = 'https://www.google.com/recaptcha/api/siteverify'
            values = {
                'secret': settings.GOOGLE_RECAPTCHA_SECRET_KEY,
                'response': recaptcha_response
            }
            data = urllib.parse.urlencode(values).encode()
            req =  urllib.request.Request(url, data=data)
            response = urllib.request.urlopen(req)
            result = json.loads(response.read().decode())
            ''' End reCAPTCHA validation '''

            if result['success']:
                form.save()
            else:
                pass

            return redirect('comments')
    else:
        form = SignUpForm()

    return render(request, 'registration/register.html', {'form': form})
