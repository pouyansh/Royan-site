from django.urls import reverse_lazy, reverse
from django.views.generic import CreateView, DetailView

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


class MessageDetails(CreateView):
    model = Message
    template_name = "message/message_details.html"
    form_class = CreateMessageForm
    success_url = reverse_lazy("dashboard:dashboard")

    def dispatch(self, request, *args, **kwargs):
        if not Message.objects.filter(id=self.kwargs['pk']):
            return reverse("index:index")
        msg = Message.objects.get(id=self.kwargs['pk'])
        if self.request.user.is_authenticated and not self.request.user.is_superuser:
            if msg.customer.username != self.request.user.username:
                return reverse("index:index")
            else:
                msg.is_opened = True
                msg.save()
                while msg.parent:
                    msg = msg.parent
                    msg.is_opened = True
                    msg.save()
        if not self.request.user.is_authenticated:
            return reverse("index:index")

        return super(MessageDetails, self).dispatch(request, args, kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['product_categories'] = Category.objects.filter(is_active=True).order_by('id')
        context['services'] = Service.objects.all().order_by('id')
        context['service_fields'] = Field.objects.all().order_by('id')
        context['research_areas'] = ResearchArea.objects.all().order_by('id')
        context['tutorials'] = Tutorial.objects.all().order_by('id')
        msg = Message.objects.get(id=self.kwargs['pk'])
        context['message'] = msg
        parents = []
        parent_msg = msg
        while parent_msg.parent:
            parent_msg = parent_msg.parent
            parents.append(parent_msg)
        parents.reverse()
        context['parents'] = parents
        return context

    def form_valid(self, form):
        msg = Message.objects.get(id=self.kwargs['pk'])
        form.instance.customer = msg.customer
        if self.request.user.is_superuser:
            form.instance.is_sender = False
        else:
            form.instance.is_sender = True
        form.instance.parent = msg
        return super(MessageDetails, self).form_valid(form)
