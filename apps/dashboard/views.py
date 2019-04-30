from django.shortcuts import redirect
from django.views.generic import TemplateView

from apps.order_service.models import OrderService
from apps.product.models import Category
from apps.registration.models import Customer, Person, Organization
from apps.research.models import ResearchArea
from apps.service.models import *
from apps.tutorial.models import Tutorial


class CustomerDashboard(TemplateView):
    template_name = 'dashboard/dashboard.html'

    def dispatch(self, request, *args, **kwargs):
        if self.request.user.is_superuser:
            return redirect('index:index')
        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['product_categories'] = Category.objects.filter(is_active=True).order_by('id')
        context['services'] = Service.objects.all().order_by('id')
        context['service_fields'] = Field.objects.all().order_by('id')
        context['research_areas'] = ResearchArea.objects.all().order_by('id')
        context['tutorials'] = Tutorial.objects.all().order_by('id')
        customer = Customer.objects.get(username=self.request.user.username)
        context['logged_in_customer'] = customer
        if customer.is_person:
            context['logged_in_user'] = Person.objects.get(username=self.request.user.username)
        else:
            context['logged_in_user'] = Organization.objects.get(username=self.request.user.username)
        context['orders'] = OrderService.objects.filter(customer=customer)
        return context
