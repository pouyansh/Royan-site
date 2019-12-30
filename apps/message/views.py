from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.mail import send_mail
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import CreateView

from apps.message.forms import *
from apps.message.models import Message
from apps.product.models import Category
from apps.registration.models import Customer
from apps.research.models import ResearchArea
from apps.royan_admin.models import RoyanTucagene
from apps.service.models import Service, Field, Field2
from apps.tutorial.models import Tutorial


class CustomerCreateMessage(LoginRequiredMixin, CreateView):
    model = Message
    form_class = CreateMessageForm
    template_name = "message/create_message.html"
    success_url = reverse_lazy("dashboard:dashboard")

    def dispatch(self, request, *args, **kwargs):
        if self.request.user.is_superuser:
            return render(request, "temporary/show_text.html", {'text': "این صفحه مخصوص کاربران است"})
        return super(CustomerCreateMessage, self).dispatch(request, args, kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['RoyanTucagene'] = RoyanTucagene.objects.all()[0]
        context['product_categories'] = Category.objects.filter(is_active=True).order_by('id')
        context['services'] = Service.objects.all().order_by('id')
        context['service_fields'] = Field.objects.all().order_by('id')
        context['research_areas'] = ResearchArea.objects.all().order_by('id')
        context['tutorials'] = Tutorial.objects.all().order_by('id')
        context['fields2'] = Field2.objects.all().order_by('id')
        return context

    def form_valid(self, form):
        form.instance.customer = Customer.objects.get(username=self.request.user.username)
        form.instance.is_sender = True
        mail_text = "username: " + self.request.user.username + "\ntext:\n" + form.instance.text
        send_mail('پیام جدید', mail_text, 'Royan TuCAGene', [RoyanTucagene.objects.all()[0].email])
        return super(CustomerCreateMessage, self).form_valid(form)


class AdminCreateMessage(LoginRequiredMixin, CreateView):
    model = Message
    form_class = CreateMessageForm
    template_name = "message/create_message_admin.html"
    success_url = reverse_lazy("royan_admin:admin_panel")

    def dispatch(self, request, *args, **kwargs):
        if not Customer.objects.filter(username=self.kwargs['username']):
            return render(request, "temporary/show_text.html", {'text': "کاربر مورد نظر یافت نشد"})
        return super(AdminCreateMessage, self).dispatch(request, args, kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['RoyanTucagene'] = RoyanTucagene.objects.all()[0]
        context['product_categories'] = Category.objects.filter(is_active=True).order_by('id')
        context['services'] = Service.objects.all().order_by('id')
        context['service_fields'] = Field.objects.all().order_by('id')
        context['research_areas'] = ResearchArea.objects.all().order_by('id')
        context['tutorials'] = Tutorial.objects.all().order_by('id')
        context['customer'] = Customer.objects.get(username=self.kwargs['username'])
        context['fields2'] = Field2.objects.all().order_by('id')
        return context

    def form_valid(self, form):
        form.instance.customer = Customer.objects.get(username=self.kwargs['username'])
        form.instance.is_sender = False
        return super(AdminCreateMessage, self).form_valid(form)


class MessageDetails(LoginRequiredMixin, CreateView):
    model = Message
    template_name = "message/message_details.html"
    form_class = CreateMessageForm
    success_url = reverse_lazy("dashboard:dashboard")

    def dispatch(self, request, *args, **kwargs):
        try:
            int(self.kwargs['pk'])
        except:
            return render(request, "temporary/show_text.html", {'text': "پیام مورد نظر یافت نشد"})
        if not self.request.user.is_superuser \
                and len(Message.objects.filter(customer__username=self.request.user.username)) < int(self.kwargs['pk']):
            return render(request, "temporary/show_text.html", {'text': "پیام مورد نظر یافت نشد"})
        if self.request.user.is_superuser \
                and len(Message.objects.all()) < int(self.kwargs['pk']):
            return render(request, "temporary/show_text.html", {'text': "پیام مورد نظر یافت نشد"})
        if self.request.user.is_superuser:
            msg = Message.objects.all().order_by('id')[int(self.kwargs['pk']) - 1]
        else:
            msg = Message.objects.filter(customer__username=self.request.user.username).order_by('id')[
                int(self.kwargs['pk']) - 1]
        if self.request.user.is_authenticated and not self.request.user.is_superuser:
            if msg.customer.username != self.request.user.username:
                return render(request, "temporary/show_text.html",
                              {'text': "کاربر گرامی شما اجازه دسترسی به این پیام را ندارید"})
            else:
                if not msg.is_sender:
                    msg.is_opened = True
                    msg.save()
                while msg.parent:
                    msg = msg.parent
                    if not msg.is_sender:
                        msg.is_opened = True
                        msg.save()
        if self.request.user.is_superuser:
            if msg.is_sender:
                msg.is_opened = True
                msg.save()
            while msg.parent:
                msg = msg.parent
                if msg.is_sender:
                    msg.is_opened = True
                    msg.save()
        return super(MessageDetails, self).dispatch(request, args, kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['RoyanTucagene'] = RoyanTucagene.objects.all()[0]
        context['product_categories'] = Category.objects.filter(is_active=True).order_by('id')
        context['services'] = Service.objects.all().order_by('id')
        context['service_fields'] = Field.objects.all().order_by('id')
        context['research_areas'] = ResearchArea.objects.all().order_by('id')
        context['tutorials'] = Tutorial.objects.all().order_by('id')
        if self.request.user.is_superuser:
            msg = Message.objects.all().order_by('id')[int(self.kwargs['pk']) - 1]
        else:
            msg = Message.objects.filter(customer__username=self.request.user.username).order_by('id')[
                int(self.kwargs['pk']) - 1]
        context['message'] = msg
        parents = []
        parent_msg = msg
        while parent_msg.parent:
            parent_msg = parent_msg.parent
            parents.append(parent_msg)
        parents.reverse()
        context['parents'] = parents
        context['fields2'] = Field2.objects.all().order_by('id')
        return context

    def form_valid(self, form):
        if self.request.user.is_superuser:
            msg = Message.objects.all().order_by('id')[int(self.kwargs['pk']) - 1]
        else:
            msg = Message.objects.filter(customer__username=self.request.user.username).order_by('id')[
                int(self.kwargs['pk']) - 1]
        form.instance.customer = msg.customer
        if self.request.user.is_superuser:
            form.instance.is_sender = False
        else:
            form.instance.is_sender = True
        form.instance.parent = msg
        return super(MessageDetails, self).form_valid(form)
