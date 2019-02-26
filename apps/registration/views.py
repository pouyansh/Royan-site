from django.shortcuts import render

from django.views.generic import CreateView

from apps.registration.forms import *


class Register(CreateView):
    form_class = SignUpForm
    template_name = 'registration/register.html'
    success_url = 'registration:register'

    def form_valid(self, form):
        customer = form.save()
        customer_type = form.type
        print("type: ", customer_type)
        if customer_type == 1:
            national_id = form.national_id
            education = form.education
            org = form.org
            cellphone_number = form.cellphone_number
            person = Person(national_id=national_id, education=education, org=org, cellphone_number=cellphone_number,
                            customer=customer)
            person.save()
