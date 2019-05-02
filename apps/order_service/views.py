import csv

import jdatetime
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import redirect, render
from django.urls import reverse_lazy
from django.views.generic import FormView, TemplateView
import xlrd

from apps.order_service.forms import *
from apps.order_service.models import *
from apps.product.models import Category
from apps.registration.models import Person, Organization, Customer
from apps.research.models import ResearchArea
from apps.service.models import Service, Field
from apps.tutorial.models import Tutorial


class StartOrderService(LoginRequiredMixin, TemplateView):
    template_name = "order_service/start_order.html"

    def dispatch(self, request, *args, **kwargs):
        if not Service.objects.filter(id=self.kwargs['pk']):
            return redirect('index:index')
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
        if not self.request.user.is_superuser:
            customer = Customer.objects.get(username=self.request.user.username)
            context['logged_in_customer'] = customer
            if customer.is_person:
                context['logged_in_user'] = Person.objects.get(username=self.request.user.username)
            else:
                context['logged_in_user'] = Organization.objects.get(username=self.request.user.username)
        service = Service.objects.get(id=self.kwargs['pk'])
        context['service'] = service
        return context


class SubmitOrderService(LoginRequiredMixin, FormView):
    form_class = OrderServiceFrom
    template_name = 'order_service/order_service.html'
    success_url = reverse_lazy('index:index')

    def dispatch(self, request, *args, **kwargs):
        if not Service.objects.filter(id=self.kwargs['pk']):
            return redirect('index:index')
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
        if not self.request.user.is_superuser:
            customer = Customer.objects.get(username=self.request.user.username)
            context['logged_in_customer'] = customer
            if customer.is_person:
                context['logged_in_user'] = Person.objects.get(username=self.request.user.username)
            else:
                context['logged_in_user'] = Organization.objects.get(username=self.request.user.username)
        service = Service.objects.get(id=self.kwargs['pk'])
        context['service'] = service
        if not self.request.user.is_superuser:
            customer = Customer.objects.get(username=self.request.user.username)
            orders = OrderService.objects.filter(customer=customer, service=service, is_finished=False)
        else:
            orders = []
        if orders:
            order = orders[0]
            content = csv.reader(open(order.file.path, 'r'))
            order.file.close()
        else:

            content = []
        context['data'] = content
        return context

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        service = Service.objects.get(id=self.kwargs['pk'])
        content = csv.reader(open(service.fields.path, 'r'))
        data = []
        for row in content:
            temp = [row[0], row[1], row[2]]
            if row[1] in ["text", "oligo"]:
                temp.append(row[3])
            if row[1] == "choice":
                tempchoices = []
                for i in range(3, len(row)):
                    if row[i]:
                        tempchoices.append((row[i], row[i]))
                temp.append(tempchoices)
            data.append(temp)
        kwargs['columns'] = data
        return kwargs

    def form_valid(self, form):
        final = form.cleaned_data['final']
        order_id = form.cleaned_data['order_id']
        service = Service.objects.get(id=self.kwargs['pk'])
        if not self.request.user.is_superuser:
            customer = Customer.objects.get(username=self.request.user.username)
            orders = OrderService.objects.filter(customer=customer, service=service, is_finished=False)
        else:
            orders = []
        if orders:
            order = orders[0]
            content = csv.reader(open(order.file.path, 'r'))
            order.file.close()
            content_data = []
            for row in content:
                content_data.append(row)
        else:
            customer = Customer.objects.get(username=self.request.user.username)
            order = OrderService(customer=customer, service=service)
            order.save()
            content_data = []
        if str(final) == "1":
            order_type = form.cleaned_data['type']
            data = []
            if '2' in order_type:
                for row in content_data:
                    data.append(row)
            if '1' in order_type:
                content = form.cleaned_data['file'].read()
                book = xlrd.open_workbook(file_contents=content)
                sheet = book.sheet_by_index(0)
                fields = []
                for j in range(1, sheet.ncols):
                    if sheet.cell_value(1, j):
                        fields.append(sheet.cell_value(1, j))
                for i in range(2, sheet.nrows):
                    row = []
                    for j in range(1, sheet.ncols):
                        if sheet.cell_value(i, j):
                            row.append(sheet.cell_value(i, j))
                    if len(row) == len(fields):
                        data.append(row)
                with open(order.file.path, 'w') as f:
                    writer = csv.writer(f)
                    for row in data:
                        writer.writerow(row)
            self.success_url = reverse_lazy('order_service:check_data', kwargs={'pk': self.kwargs['pk']})
        else:
            try:
                if order_id != -1:
                    with open(order.file.path, 'w+') as f:
                        f.truncate()
                        writer = csv.writer(f)
                        for i in range(len(content_data)):
                            if i != order_id - 1:
                                writer.writerow(content_data[i])
                else:
                    fields = csv.reader(open(service.fields.path, 'r'))
                    data = []
                    for row in fields:
                        data.append(form.cleaned_data[row[0]])
                    content_data.append(data)

                    with open(order.file.path, 'a') as f:
                        writer = csv.writer(f)
                        writer.writerow(data)
            except:
                with open(order.file.path, 'w') as f:
                    writer = csv.writer(f)
                    for row in content_data:
                        writer.writerow(row)
            self.success_url = reverse_lazy('order_service:order_service', kwargs={'pk': self.kwargs['pk']})
        return super(SubmitOrderService, self).form_valid(form)


class CheckData(LoginRequiredMixin, FormView):
    form_class = CheckDataFrom
    template_name = "order_service/check_data.html"
    success_url = reverse_lazy("index:index")

    def dispatch(self, request, *args, **kwargs):
        if not Service.objects.filter(id=self.kwargs['pk']):
            return redirect('index:index')
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
        if not self.request.user.is_superuser:
            customer = Customer.objects.get(username=self.request.user.username)
            context['logged_in_customer'] = customer
            if customer.is_person:
                context['logged_in_user'] = Person.objects.get(username=self.request.user.username)
            else:
                context['logged_in_user'] = Organization.objects.get(username=self.request.user.username)
        service = Service.objects.get(id=self.kwargs['pk'])
        context['service'] = service
        fields_file = csv.reader(open(service.fields.path, 'r'))
        fields = []
        for row in fields_file:
            fields.append(row[2])
        context['fields'] = fields
        if not self.request.user.is_superuser:
            customer = Customer.objects.get(username=self.request.user.username)
            orders = OrderService.objects.filter(customer=customer, service=service, is_finished=False)
        else:
            orders = []
        if orders:
            order = orders[0]
            content = csv.reader(open(order.file.path, 'r'))
            order.file.close()
        else:
            content = []
        context['data'] = content
        return context

    def form_valid(self, form):
        service = Service.objects.get(id=self.kwargs['pk'])
        customer = Customer.objects.get(username=self.request.user.username)
        orders = OrderService.objects.filter(customer=customer, service=service, is_finished=False)
        order = orders[0]
        order.is_finished = True
        order.name = form.cleaned_data['name']
        code = service.name + "-" + str(jdatetime.datetime.now().date()) + "-" + str(order.id)
        order.code = code
        order.date = jdatetime.datetime.now()
        order.save()
        self.success_url = reverse_lazy('order_service:get_code', kwargs={'pk': order.id})
        return super(CheckData, self).form_valid(form)


class GetCode(LoginRequiredMixin, TemplateView):
    template_name = "order_service/get_code.html"

    def dispatch(self, request, *args, **kwargs):
        if not OrderService.objects.filter(id=self.kwargs['pk']):
            return redirect('index:index')
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
        if not self.request.user.is_superuser:
            customer = Customer.objects.get(username=self.request.user.username)
            context['logged_in_customer'] = customer
            if customer.is_person:
                context['logged_in_user'] = Person.objects.get(username=self.request.user.username)
            else:
                context['logged_in_user'] = Organization.objects.get(username=self.request.user.username)
        order = OrderService.objects.get(id=self.kwargs['pk'])
        context['code'] = order.code
        return context


class OrderDetails(LoginRequiredMixin, TemplateView):
    template_name = "order_service/order_details.html"

    def dispatch(self, request, *args, **kwargs):
        try:
            int(self.kwargs['pk'])
        except:
            return render(request, "temporary/show_text.html", {'text': "سفارش مورد نظر یافت نشد"})
        if self.request.user.is_superuser:
            if len(OrderService.objects.all()) < int(self.kwargs['pk']):
                return render(request, "temporary/show_text.html", {'text': "سفارش مورد نظر یافت نشد"})
        else:
            if len(OrderService.objects.filter(customer__username=self.request.user.username)) < int(self.kwargs['pk']):
                return render(request, "temporary/show_text.html", {'text': "سفارش مورد نظر یافت نشد"})
        return super().dispatch(request, *args, **kwargs)

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
        if self.request.user.is_superuser:
            order = OrderService.objects.all().order_by('id')[int(self.kwargs['pk']) - 1]
        else:
            order = OrderService.objects.filter(customer__username=self.request.user.username).order_by('id')[
                int(self.kwargs['pk']) - 1]
        context['order'] = order
        service = order.service
        context['service'] = service
        with open(service.fields.path, 'r') as f:
            fields_file = csv.reader(f)
            fields = []
            for row in fields_file:
                fields.append(row[2])
            context['fields'] = fields
        with open(order.file.path, 'r') as f:
            content = csv.reader(f)
            data = []
            for row in content:
                data.append(row)
            context['data'] = data
        context['order_id'] = self.kwargs['pk']
        return context


class CheckReceived(LoginRequiredMixin, TemplateView):
    template_name = "temporary/show_text.html"

    def dispatch(self, request, *args, **kwargs):
        try:
            int(self.kwargs['pk'])
        except:
            return render(request, "temporary/show_text.html", {'text': "سفارش مورد نظر یافت نشد"})
        if self.request.user.is_superuser:
            if len(OrderService.objects.all()) < int(self.kwargs['pk']):
                return render(request, "temporary/show_text.html", {'text': "سفارش مورد نظر یافت نشد"})
        else:
            if len(OrderService.objects.filter(customer__username=self.request.user.username)) < int(self.kwargs['pk']):
                return render(request, "temporary/show_text.html", {'text': "سفارش مورد نظر یافت نشد"})
        if self.request.user.is_superuser:
            order = OrderService.objects.all().order_by('id')[int(self.kwargs['pk']) - 1]
        else:
            order = OrderService.objects.filter(customer__username=self.request.user.username).order_by('id')[
                int(self.kwargs['pk']) - 1]
        if not order.is_finished or not order.invoice:
            return render(request, "temporary/show_text.html", {'text': "سفارش مورد نظر به مرحله تحویل نرسیده است."})
        order.received = True
        order.save()
        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.request.user.is_superuser:
            order = OrderService.objects.all().order_by('id')[int(self.kwargs['pk']) - 1]
        else:
            order = OrderService.objects.filter(customer__username=self.request.user.username).order_by('id')[
                int(self.kwargs['pk']) - 1]
        context[
            'text'] = "کاربر گرامی، سفارش مد نظر شما به کد " + order.code + " در وضعیت تحویل گرفته شده قرار داده شد."
        return context
