from django.contrib.auth.models import User
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.views.generic import TemplateView, FormView, UpdateView

from apps.message.models import Message
from apps.order_service.models import OrderService
from apps.product.models import Category
from apps.registration.models import Customer, Person, Organization
from apps.research.models import ResearchArea
from apps.royan_admin.forms import ChangeSystemInfoForm, BlockForm
from apps.royan_admin.models import RoyanTucagene
from apps.service.models import *
from apps.tutorial.models import Tutorial


class AdminPanel(TemplateView):
    template_name = 'royan_admin/admin_panel.html'

    def get_context_data(self, **kwargs):
        context = super(AdminPanel, self).get_context_data()
        context['RoyanTucagene'] = RoyanTucagene.objects.all()[0]
        context['product_categories'] = Category.objects.filter(is_active=True).order_by('id')
        context['admin'] = self.request.user
        context['services'] = Service.objects.all().order_by('id')
        context['service_fields'] = Field.objects.all().order_by('id')
        context['research_areas'] = ResearchArea.objects.all().order_by('id')
        context['tutorials'] = Tutorial.objects.all().order_by('id')
        context['fields2'] = Field2.objects.all().order_by('id')
        all_orders = OrderService.objects.all().order_by('id')
        orders = OrderService.objects.filter(is_finished=True, invoice=True, received=True,
                                             payed=True).order_by('id')
        order_list = []
        index = 0
        index_all = 0
        while index < len(orders):
            if orders[index] == all_orders[index_all]:
                order_list.append([orders[index], index_all + 1])
                index += 1
            index_all += 1
        context['finished_orders'] = order_list
        orders = OrderService.objects.filter(is_finished=True, invoice=True, payed=False).order_by(
            'id')
        order_list = []
        index = 0
        index_all = 0
        while index < len(orders):
            if orders[index] == all_orders[index_all]:
                order_list.append([orders[index], index_all + 1])
                index += 1
            index_all += 1
        context['orders_not_payed'] = order_list
        orders = OrderService.objects.filter(is_finished=True, invoice=True,
                                             received=False).order_by('id')
        order_list = []
        index = 0
        index_all = 0
        while index < len(orders):
            if orders[index] == all_orders[index_all]:
                order_list.append([orders[index], index_all + 1])
                index += 1
            index_all += 1
        context['orders_not_received'] = order_list
        orders = OrderService.objects.filter(is_finished=True, invoice=False).order_by('id')
        order_list = []
        index = 0
        index_all = 0
        while index < len(orders):
            if orders[index] == all_orders[index_all]:
                order_list.append([orders[index], index_all + 1])
                index += 1
            index_all += 1
        context['orders_not_invoice'] = order_list
        orders = OrderService.objects.filter(is_finished=False).order_by('id')
        order_list = []
        index = 0
        index_all = 0
        while index < len(orders):
            if orders[index] == all_orders[index_all]:
                order_list.append([orders[index], index_all + 1])
                index += 1
            index_all += 1
        context['orders_not_finished'] = order_list
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
        context['RoyanTucagene'] = RoyanTucagene.objects.all()[0]
        context['product_categories'] = Category.objects.filter(is_active=True).order_by('id')
        context['services'] = Service.objects.all().order_by('id')
        context['service_fields'] = Field.objects.all().order_by('id')
        context['research_areas'] = ResearchArea.objects.all().order_by('id')
        context['tutorials'] = Tutorial.objects.all().order_by('id')
        context['fields2'] = Field2.objects.all().order_by('id')
        customer = Customer.objects.get(id=self.kwargs['pk'])
        context['logged_in_customer'] = customer
        if customer.is_person:
            context['logged_in_user'] = Person.objects.get(username=customer.username)
        else:
            context['logged_in_user'] = Organization.objects.get(username=customer.username)
        orders = OrderService.objects.filter(customer=customer).order_by('id')
        context['orders'] = orders
        all_orders = OrderService.objects.all().order_by('id')
        index_list = []
        index = 0
        index_all = 0
        while index < len(orders):
            if orders[index] == all_orders[index_all]:
                index_list.append([orders[index], index_all + 1])
                index += 1
            index_all += 1
        context['index_list'] = index_list
        all_messages = Message.objects.all().order_by('-id')
        messages = Message.objects.filter(customer=customer).order_by('-id')
        index_list = []
        index = 0
        index_all = 0
        while index < len(messages):
            if messages[index] == all_messages[index_all]:
                index_list.append([messages[index], index_all + 1])
                index += 1
            index_all += 1
        context['messages'] = index_list
        return context


class ChangeSystemInformation(UpdateView):
    form_class = ChangeSystemInfoForm
    success_url = reverse_lazy("index:index")
    model = RoyanTucagene
    template_name = "royan_admin/update_info.html"

    def get_context_data(self, **kwargs):
        context = super(ChangeSystemInformation, self).get_context_data()
        context['RoyanTucagene'] = RoyanTucagene.objects.all()[0]
        context['product_categories'] = Category.objects.filter(is_active=True).order_by('id')
        context['admin'] = self.request.user
        context['services'] = Service.objects.all().order_by('id')
        context['service_fields'] = Field.objects.all().order_by('id')
        context['research_areas'] = ResearchArea.objects.all().order_by('id')
        context['tutorials'] = Tutorial.objects.all().order_by('id')
        context['fields2'] = Field2.objects.all().order_by('id')
        return context


class BlockUser(FormView):
    template_name = "royan_admin/block_user.html"
    success_url = reverse_lazy("royan_admin:blocked")
    form_class = BlockForm

    def get_context_data(self, **kwargs):
        context = super(BlockUser, self).get_context_data(**kwargs)
        context['RoyanTucagene'] = RoyanTucagene.objects.all()[0]
        context['product_categories'] = Category.objects.filter(is_active=True).order_by('id')
        context['admin'] = self.request.user
        context['services'] = Service.objects.all().order_by('id')
        context['service_fields'] = Field.objects.all().order_by('id')
        context['research_areas'] = ResearchArea.objects.all().order_by('id')
        context['tutorials'] = Tutorial.objects.all().order_by('id')
        context['user'] = User.objects.get(id=self.kwargs['pk'])
        context['fields2'] = Field2.objects.all().order_by('id')
        return context

    def form_valid(self, form):
        user = User.objects.get(id=self.kwargs['pk'])
        print(user.is_active)
        user.is_active = False
        user.save()
        return super(BlockUser, self).form_valid(form)


class BlockSuccessful(TemplateView):
    template_name = 'temporary/show_text.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['RoyanTucagene'] = RoyanTucagene.objects.all()[0]
        context['product_categories'] = Category.objects.filter(is_active=True).order_by('id')
        context['services'] = Service.objects.all().order_by('id')
        context['service_fields'] = Field.objects.all().order_by('id')
        context['research_areas'] = ResearchArea.objects.all().order_by('id')
        context['tutorials'] = Tutorial.objects.all().order_by('id')
        context['fields2'] = Field2.objects.all().order_by('id')
        context[
            'text'] = "کاربر مورد نظر بلاک شد"
        return context

