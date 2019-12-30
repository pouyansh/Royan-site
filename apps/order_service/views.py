import csv
import os

import jdatetime
import xlrd
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.files.base import ContentFile
from django.core.mail import send_mail
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import FormView, TemplateView

from apps.order_service.forms import *
from apps.order_service.models import *
from apps.product.models import Category
from apps.registration.models import Person, Organization, Customer
from apps.research.models import ResearchArea
from apps.royan_admin.models import RoyanTucagene
from apps.service.models import Service, Field, Field2
from apps.tutorial.models import Tutorial


class StartOrderService(LoginRequiredMixin, TemplateView):
    template_name = "order_service/start_order.html"

    def dispatch(self, request, *args, **kwargs):
        try:
            int(self.kwargs['pk'])
        except:
            return render(request, "temporary/show_text.html", {'text': "سرویس مورد نظر یافت نشد"})
        if not Service.objects.filter(id=self.kwargs['pk']):
            return render(request, "temporary/show_text.html", {'text': "سرویس مورد نظر یافت نشد"})
        if self.request.user.is_superuser:
            return render(request, "temporary/show_text.html", {'text': "ثبت سفارش مخصوص مشتریان است"})
        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['RoyanTucagene'] = RoyanTucagene.objects.all()[0]
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
        service = Service.objects.get(id=self.kwargs['pk'])
        context['service'] = service
        context['fields2'] = Field2.objects.all().order_by('id')
        return context


class SubmitOrderService(LoginRequiredMixin, FormView):
    form_class = OrderServiceFrom
    template_name = 'order_service/order_service.html'
    success_url = reverse_lazy('index:index')

    def dispatch(self, request, *args, **kwargs):
        try:
            int(self.kwargs['pk'])
        except:
            return render(request, "temporary/show_text.html", {'text': "سرویس مورد نظر یافت نشد"})
        if not Service.objects.filter(id=self.kwargs['pk']):
            return render(request, "temporary/show_text.html", {'text': "سرویس مورد نظر یافت نشد"})
        if self.request.user.is_superuser:
            return render(request, "temporary/show_text.html", {'text': "ثبت سفارش مخصوص مشتریان است"})
        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['RoyanTucagene'] = RoyanTucagene.objects.all()[0]
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
        service = Service.objects.get(id=self.kwargs['pk'])
        context['service'] = service
        customer = Customer.objects.get(username=self.request.user.username)
        orders = OrderService.objects.filter(customer=customer, service=service, is_finished=False)
        if orders:
            order = orders[0]
            content = csv.reader(open(order.file.path, 'r'))
            order.file.close()
        else:
            content = []
        context['data'] = content
        context['fields2'] = Field2.objects.all().order_by('id')
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
        customer = Customer.objects.get(username=self.request.user.username)
        orders = OrderService.objects.filter(customer=customer, service=service, is_finished=False)
        if orders:
            order = orders[0]
            content = csv.reader(open(order.file.path, 'r'))
            order.file.close()
            content_data = []
            for row in content:
                content_data.append(row)
        else:
            order = OrderService(customer=customer, service=service)
            order.save()
            if not os.path.exists("media/orders/"):
                os.mkdir("media/orders/")
            if not os.path.exists("media/orders/user_" + str(customer.username)):
                os.mkdir("media/orders/user_" + str(customer.username))
            if not os.path.exists("media/orders/user_" + str(customer.username) + "/service_" + str(service.id)):
                os.mkdir("media/orders/user_" + str(customer.username) + "/service_" + str(service.id))
            f = open("media/orders/user_" + str(customer.username) + "/service_" + str(service.id) + "/order_" + str(
                order.id) + ".csv", "x")
            f.close()
            order.file.save(
                "media/orders/user_" + str(customer.username) + "/service_" + str(service.id) + "/order_" + str(
                    order.id) + ".csv", ContentFile(''), save=True)
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
                index = 0
                while True:
                    check = 0
                    for j in range(sheet.ncols):
                        if sheet.cell_value(index, j):
                            check += 1
                    if check >= 2:
                        break
                    index += 1
                for j in range(1, sheet.ncols):
                    if sheet.cell_value(index, j):
                        fields.append(sheet.cell_value(index, j))
                index += 1
                for i in range(index, sheet.nrows):
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
        try:
            int(self.kwargs['pk'])
        except:
            return render(request, "temporary/show_text.html", {'text': "سرویس مورد نظر یافت نشد"})
        if not Service.objects.filter(id=self.kwargs['pk']):
            return render(request, "temporary/show_text.html", {'text': "سرویس مورد نظر یافت نشد"})
        if self.request.user.is_superuser:
            return render(request, "temporary/show_text.html", {'text': "ثبت سفارش مخصوص مشتریان است"})
        service = Service.objects.get(id=self.kwargs['pk'])
        customer = Customer.objects.get(username=self.request.user.username)
        if not OrderService.objects.filter(customer=customer, service=service, is_finished=False):
            return render(request, "temporary/show_text.html",
                          {'text': "شما سفارش تکمیل نشده‌ای برای این سرویس ندارید"})
        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['RoyanTucagene'] = RoyanTucagene.objects.all()[0]
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
        service = Service.objects.get(id=self.kwargs['pk'])
        context['service'] = service
        fields_file = csv.reader(open(service.fields.path, 'r'))
        fields = []
        for row in fields_file:
            fields.append(row[2])
        context['fields'] = fields
        orders = OrderService.objects.filter(customer=customer, service=service, is_finished=False)
        order = orders[0]
        content = csv.reader(open(order.file.path, 'r'))
        order.file.close()
        context['data'] = content
        context['fields2'] = Field2.objects.all().order_by('id')
        return context

    def form_valid(self, form):
        service = Service.objects.get(id=self.kwargs['pk'])
        customer = Customer.objects.get(username=self.request.user.username)
        orders = OrderService.objects.filter(customer=customer, service=service, is_finished=False)
        order = orders[0]
        index = 0
        all_orders = OrderService.objects.filter(customer=customer).order_by('id')
        while all_orders[index] != order:
            index += 1
        order.is_finished = True
        order.name = form.cleaned_data['name']
        code = service.name + "-" + str(jdatetime.datetime.now().date()) + "-" + str(index)
        order.code = code
        order.date = jdatetime.datetime.now()
        order.save()
        mail_text = "با سلام،\nکاربر با نام "
        if customer.is_person:
            mail_text += customer.name + " " + customer.last_name
        else:
            mail_text += customer.last_name
        mail_text += " و نام کاربری " + customer.username + " سفارش با شناسه " + order.code + "ثبت کرد. "
        mail_text += "برای مشاهده جزئیات، برروی لینک زیر کلیک کنید."
        mail_text += "\nhttp://www.royantucagene.com/admin_panel"
        send_mail('ثبت سفارش', mail_text, 'Royan TuCAGene', [RoyanTucagene.objects.all()[0].email])
        self.success_url = reverse_lazy('order_service:get_code', kwargs={'pk': index})
        return super(CheckData, self).form_valid(form)


class GetCode(LoginRequiredMixin, TemplateView):
    template_name = "order_service/get_code.html"

    def dispatch(self, request, *args, **kwargs):
        if self.request.user.is_superuser:
            return render(request, "temporary/show_text.html", {'text': "ثبت سفارش مخصوص مشتریان است"})
        try:
            int(self.kwargs['pk'])
        except:
            return render(request, "temporary/show_text.html", {'text': "سفارش مورد نظر یافت نشد"})
        if len(OrderService.objects.filter(customer__username=self.request.user.username)) < int(self.kwargs['pk']):
            return render(request, "temporary/show_text.html", {'text': "سفارش مورد نظر یافت نشد"})
        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['RoyanTucagene'] = RoyanTucagene.objects.all()[0]
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
        order = OrderService.objects.filter(customer__username=self.request.user.username).order_by('id')[
            int(self.kwargs['pk'])]
        context['code'] = order.code
        context['fields2'] = Field2.objects.all().order_by('id')
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
        context['RoyanTucagene'] = RoyanTucagene.objects.all()[0]
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
        context['fields2'] = Field2.objects.all().order_by('id')
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
        context['fields2'] = Field2.objects.all().order_by('id')
        mail_text = 'با سلام،\nکاربر با نام'
        if self.request.user.customer.is_person:
            mail_text += self.request.user.customer.name + " " + self.request.user.customer.last_name
        else:
            mail_text += self.request.user.customer.last_name
        mail_text += "و نام کاربری " + self.request.user.username + "سفارش با شناسه " + order.code +\
                     "را در وضعیت تحویل گرفته شده قرار داد. "
        mail_text += "برای مشاهده جزئیات، برروی لینک زیر کلیک کنید."
        mail_text += "\nhttp://www.royantucagene.com/admin_panel"
        send_mail('تغییر وضعیت سفارش', mail_text, 'Royan TuCAGene', [RoyanTucagene.objects.all()[0].email])
        return context


class CheckPayed(TemplateView):
    template_name = "temporary/show_text.html"

    def dispatch(self, request, *args, **kwargs):
        try:
            int(self.kwargs['pk'])
        except:
            return render(request, "temporary/show_text.html", {'text': "سفارش مورد نظر یافت نشد"})
        if len(OrderService.objects.all()) < int(self.kwargs['pk']):
            return render(request, "temporary/show_text.html", {'text': "سفارش مورد نظر یافت نشد"})
        order = OrderService.objects.all().order_by('id')[int(self.kwargs['pk']) - 1]
        if not order.is_finished or not order.invoice:
            return render(request, "temporary/show_text.html", {'text': "سفارش مورد نظر به مرحله پرداخت نرسیده است."})
        order.payed = True
        order.save()
        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        order = OrderService.objects.all().order_by('id')[int(self.kwargs['pk']) - 1]
        context[
            'text'] = "سفارش مد نظر شما به کد " + order.code + " در وضعیت پرداخت شده قرار داده شد."
        context['fields2'] = Field2.objects.all().order_by('id')
        mail_text = 'کاربر گرامی،\n با سلام،\n'
        mail_text += "سفارش با شناسه " + order.code + \
                     "در وضعیت پرداخت شده قرار گرفت. "
        mail_text += "برای مشاهده جزئیات، برروی لینک زیر کلیک کنید."
        mail_text += "\nhttp://www.royantucagene.com/dashboard"
        send_mail('تغییر وضعیت سفارش', mail_text, 'Royan TuCAGene', [order.customer.email])
        return context


class SetInvoice(FormView):
    form_class = SetInvoiceForm
    template_name = "order_service/set_invoice.html"

    def dispatch(self, request, *args, **kwargs):
        try:
            int(self.kwargs['pk'])
        except:
            return render(request, "temporary/show_text.html", {'text': "سفارش مورد نظر یافت نشد"})
        if len(OrderService.objects.all()) < int(self.kwargs['pk']):
            return render(request, "temporary/show_text.html", {'text': "سفارش مورد نظر یافت نشد"})
        order = OrderService.objects.all().order_by('id')[int(self.kwargs['pk']) - 1]
        if not order.is_finished:
            return render(request, "temporary/show_text.html", {'text': "سفارش مورد نظر به مرحله پرداخت نرسیده است."})
        order.invoice = True
        order.save()
        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        order = OrderService.objects.all().order_by('id')[int(self.kwargs['pk']) - 1]
        context['order'] = order
        return context

    def form_valid(self, form):
        payment = form.cleaned_data['payment']
        order = OrderService.objects.all().order_by('id')[int(self.kwargs['pk']) - 1]
        order.payment = payment
        order.save()
        self.success_url = reverse_lazy("order_service:order_invoice", kwargs={'pk': self.kwargs['pk']})
        return super(SetInvoice, self).form_valid(form)


class CheckInvoice(TemplateView):
    template_name = "temporary/show_text.html"

    def dispatch(self, request, *args, **kwargs):
        try:
            int(self.kwargs['pk'])
        except:
            return render(request, "temporary/show_text.html", {'text': "سفارش مورد نظر یافت نشد"})
        if len(OrderService.objects.all()) < int(self.kwargs['pk']):
            return render(request, "temporary/show_text.html", {'text': "سفارش مورد نظر یافت نشد"})
        order = OrderService.objects.all().order_by('id')[int(self.kwargs['pk']) - 1]
        if not order.is_finished:
            return render(request, "temporary/show_text.html", {'text': "سفارش مورد نظر به مرحله پرداخت نرسیده است."})
        order.invoice = True
        order.save()
        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        order = OrderService.objects.all().order_by('id')[int(self.kwargs['pk']) - 1]
        context[
            'text'] = "تغییرات مورد نظر بر روی سفارش به کد " + order.code + " با موفقیت ثبت شد."
        return context


class SetReceivingDate(FormView):
    form_class = SetReceivingDateForm
    template_name = "order_service/set_receiving_date.html"

    def dispatch(self, request, *args, **kwargs):
        try:
            int(self.kwargs['pk'])
        except:
            return render(request, "temporary/show_text.html", {'text': "سفارش مورد نظر یافت نشد"})
        if len(OrderService.objects.all()) < int(self.kwargs['pk']):
            return render(request, "temporary/show_text.html", {'text': "سفارش مورد نظر یافت نشد"})
        order = OrderService.objects.all().order_by('id')[int(self.kwargs['pk']) - 1]
        if not order.is_finished:
            return render(request, "temporary/show_text.html", {'text': "سفارش مورد نظر به مرحله پرداخت نرسیده است."})
        order.invoice = True
        order.save()
        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        order = OrderService.objects.all().order_by('id')[int(self.kwargs['pk']) - 1]
        context['order'] = order
        return context

    def form_valid(self, form):
        receiving_date = form.cleaned_data['receiving_date']
        order = OrderService.objects.all().order_by('id')[int(self.kwargs['pk']) - 1]
        order.receiving_date = receiving_date
        order.save()
        self.success_url = reverse_lazy("order_service:order_invoice", kwargs={'pk': self.kwargs['pk']})
        return super(SetReceivingDate, self).form_valid(form)
