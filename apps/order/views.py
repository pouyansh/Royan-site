from django.urls import reverse_lazy
from django.views.generic import FormView

from apps.order.forms import *
from apps.product.models import Category
from apps.registration.models import Person, Organization, Customer
from apps.research.models import ResearchArea
from apps.service.models import Service, Field
from apps.tutorial.models import Tutorial


class SubmitOrderService(FormView):
    form_class = OrderServiceFrom
    template_name = 'order/order_service.html'
    success_url = reverse_lazy('index:index')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['product_categories'] = Category.objects.filter(is_active=True).order_by('id')
        context['services'] = Service.objects.all().order_by('id')
        context['service_fields'] = Field.objects.all().order_by('id')
        context['research_areas'] = ResearchArea.objects.all().order_by('id')
        context['tutorials'] = Tutorial.objects.all().order_by('id')
        if not self.request.user.is_superuser:
            customer = Customer.objects.get(username=self.request.user.username)
            context['logged_in_customer'] = customer
            if customer.is_person:
                context['logged_in_user'] = Person.objects.get(username=self.request.user.username)
            else:
                context['logged_in_user'] = Organization.objects.get(username=self.request.user.username)
        context['data'] = [['a1', 'm1', '0.01', 'yes', 'no'], ['a2', 'm2', '0.5', 'no', 'no'],
                           ['a3', 'm3', '0.1', 'yes', 'yes']]
        return context

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['columns'] = [['name', 'text', 'Oligo name', 20], ['sequence', 'text', 'Oligo Sequence', 20],
                             ['Concentration', 'choice', 'concentration',
                              [(1, '0.01'), (2, '0.02'), (2, '0.1'), (2, '0.5')]],
                             ['purification', 'choice', 'purification', [(1, 'yes'), (2, 'no')]],
                             ['modification', 'choice', 'modification', [(1, 'yes'), (2, 'no')]]]
        return kwargs

    def form_valid(self, form):
        print("valid", form.cleaned_data['name'])
        return super(SubmitOrderService, self).form_valid(form)

    def form_invalid(self, form):
        print("invalid", form)
        return super(SubmitOrderService, self).form_invalid(form)
