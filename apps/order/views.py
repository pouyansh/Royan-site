from django.shortcuts import render
from django.views.generic import FormView

from apps.order.forms import *


class SubmitOrderService(FormView):
    form_class = OrderServiceFrom
    template_name = 'service/order_service.html'

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['columns'] = [['name', 'text', 'نام', 30], ['seq', 'text', 'توالی', 20],
                             ['purification', 'choice', 'purification', [(1, 'yes'), (2, 'no')]]]
        return kwargs