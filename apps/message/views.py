from django.urls import reverse_lazy
from django.views.generic import CreateView

from apps.message.forms import *
from apps.message.models import Message
from apps.product.models import Category
from apps.registration.models import Customer
from apps.research.models import ResearchArea
from apps.service.models import Service, Field
from apps.tutorial.models import Tutorial


class CustomerCreateMessage(CreateView):
    model = Message
    form_class = CreateMessageForm
    template_name = "message/create_message.html"
    success_url = reverse_lazy("dashboard:dashboard")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['product_categories'] = Category.objects.filter(is_active=True).order_by('id')
        context['services'] = Service.objects.all().order_by('id')
        context['service_fields'] = Field.objects.all().order_by('id')
        context['research_areas'] = ResearchArea.objects.all().order_by('id')
        context['tutorials'] = Tutorial.objects.all().order_by('id')
        return context

    def form_valid(self, form):
        form.instance.customer = Customer.objects.get(username=self.request.user.username)
        form.instance.is_sender = True
        return super(CustomerCreateMessage, self).form_valid(form)


class AdminCreateMessage(CreateView):
    model = Message
    form_class = CreateMessageForm
    template_name = "message/create_message_admin.html"
    success_url = reverse_lazy("royan_admin:admin_panel")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['product_categories'] = Category.objects.filter(is_active=True).order_by('id')
        context['services'] = Service.objects.all().order_by('id')
        context['service_fields'] = Field.objects.all().order_by('id')
        context['research_areas'] = ResearchArea.objects.all().order_by('id')
        context['tutorials'] = Tutorial.objects.all().order_by('id')
        context['customer'] = Customer.objects.get(id=self.kwargs['pk'])
        return context

    def form_valid(self, form):
        form.instance.customer = Customer.objects.get(id=self.kwargs['pk'])
        form.instance.is_sender = False
        return super(AdminCreateMessage, self).form_valid(form)
