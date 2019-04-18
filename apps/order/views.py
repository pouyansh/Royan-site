from django.shortcuts import render
from django.views.generic import FormView

from apps.order.forms import *


class SubmitOrderService(FormView):
    form_class = OrderServiceFrom
    template_name = 'order/order_service.html'

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['columns'] = [['name', 'text', 'نام', 20], ['seq', 'text', 'توالی', 20],
                             ['Concentration', 'choice', 'concentration',
                              [(1, '0.01'), (2, '0.02'), (2, '0.1'), (2, '0.5')]],
                             ['purification', 'choice', 'purification', [(1, 'yes'), (2, 'no')]],
                             ['modification', 'choice', 'modification', [(1, 'yes'), (2, 'no')]]]
        return kwargs
