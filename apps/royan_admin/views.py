from django.shortcuts import redirect
from django.views.generic import TemplateView

from apps.message.models import Message
from apps.order_service.models import OrderService
from apps.product.models import Category
from apps.registration.models import Customer, Person, Organization
from apps.research.models import ResearchArea
from apps.service.models import *
from apps.tutorial.models import Tutorial


class AdminPanel(TemplateView):
    template_name = 'royan_admin/admin_panel.html'

    def get_context_data(self, **kwargs):
        context = super(AdminPanel, self).get_context_data()
        context['product_categories'] = Category.objects.filter(is_active=True).order_by('id')
        context['admin'] = self.request.user
        context['services'] = Service.objects.all().order_by('id')
        context['service_fields'] = Field.objects.all().order_by('id')
        context['research_areas'] = ResearchArea.objects.all().order_by('id')
        context['tutorials'] = Tutorial.objects.all().order_by('id')
        context['finished_orders'] = OrderService.objects.filter(is_finished=True, invoice=True, received=True,
                                                                 payed=True).order_by('id')
        context['orders_not_payed'] = OrderService.objects.filter(is_finished=True, invoice=True, payed=False).order_by(
            'id')
        context['orders_not_received'] = OrderService.objects.filter(is_finished=True, invoice=True,
                                                                     received=False).order_by('id')
        context['orders_not_invoice'] = OrderService.objects.filter(is_finished=True, invoice=False).order_by('id')
        context['orders_not_finished'] = OrderService.objects.filter(is_finished=False).order_by('id')
        context['messages'] = Message.objects.all().order_by('-id')
        context['customers'] = Customer.objects.all().order_by('-id')
        return context


class CustomerDetails(TemplateView):
    template_name = 'royan_admin/customer_profile.html'

    def dispatch(self, request, *args, **kwargs):
        if not Customer.objects.filter(id=self.kwargs['pk']):
            return redirect('index:index')
        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['product_categories'] = Category.objects.filter(is_active=True).order_by('id')
        context['services'] = Service.objects.all().order_by('id')
        context['service_fields'] = Field.objects.all().order_by('id')
        context['research_areas'] = ResearchArea.objects.all().order_by('id')
        context['tutorials'] = Tutorial.objects.all().order_by('id')
        customer = Customer.objects.get(id=self.kwargs['pk'])
        context['logged_in_customer'] = customer
        if customer.is_person:
            context['logged_in_user'] = Person.objects.get(username=customer.username)
        else:
            context['logged_in_user'] = Organization.objects.get(username=customer.username)
        context['orders'] = OrderService.objects.filter(customer=customer).order_by('id')
        context['messages'] = Message.objects.filter(customer=customer).order_by('-id')
        return context
