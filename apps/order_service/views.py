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
        context['fields2'] = Field2.objects.all().order_by('id')
        return context

    def form_valid(self, form):
        service = Service.objects.get(id=self.kwargs['pk'])
        customer = Customer.objects.get(username=self.request.user.username)

        number_constraints = ["Sample Concentration (ng/ul)", "product size (bp)", "Primer Concentration (pmol/ul)"]
        oligo_constraints = ["Primer Sequence (5 to 3)"]
        oligo_letters = "ACGTNRYSWKMBDHV"

        data = []
        content = form.cleaned_data['file'].read()
        book = xlrd.open_workbook(file_contents=content)
        sheet = book.sheet_by_index(0)
        field_names = ""
        index = 1
        while True:
            if index >= sheet.ncols:
                break
            if not sheet.cell_value(2, index):
                break
            field_names += sheet.cell_value(2, index) + ";"
            index += 1
        if field_names != service.field_names:
            self.success_url = reverse_lazy('order_service:file_error_columns')
            return super(SubmitOrderService, self).form_valid(form)
        field_names = field_names.split(';')[:-1]
        row_index = 3
        while row_index < sheet.nrows:
            row = []
            check = False
            for j in range(1, sheet.ncols):
                if sheet.cell_value(row_index, j):
                    if field_names[j - 1] in number_constraints:
                        try:
                            float(sheet.cell_value(row_index, j))
                        except ValueError or TypeError:
                            self.success_url = reverse_lazy('order_service:file_error_number')
                            return super(SubmitOrderService, self).form_valid(form)
                    if field_names[j - 1] in oligo_constraints:
                        for c in sheet.cell_value(row_index, j):
                            if c not in oligo_letters:
                                self.success_url = reverse_lazy('order_service:file_error_oligo')
                                return super(SubmitOrderService, self).form_valid(form)
                    row.append(sheet.cell_value(row_index, j))
                    check = True
            if check and len(row) != len(field_names):
                self.success_url = reverse_lazy('order_service:file_error_incomplete')
                return super(SubmitOrderService, self).form_valid(form)
            row_index += 1
            if check:
                data.append(row)
        if row_index < sheet.nrows:
            self.success_url = reverse_lazy('order_service:file_error_incomplete')
            return super(SubmitOrderService, self).form_valid(form)
        order = OrderService(customer=customer, service=service)
        order.file = form.cleaned_data['file']
        order.save()
        self.success_url = reverse_lazy('order_service:check_data', kwargs={'pk': order.id})
        return super(SubmitOrderService, self).form_valid(form)


class FileErrorColumns(TemplateView):
    template_name = "temporary/show_text.html"

    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['text'] = "ستون های این فایل تغییر کرده اند و امکان آپلود این فایل وجود ندارد."
        return context


class FileErrorNumber(TemplateView):
    template_name = "temporary/show_text.html"

    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['text'] = "در ستون های " + \
                          "Sample Concentration (ng/ul), product size (bp), Primer Concentration (pmol/ul)" + \
                          " تنها مقادیر عددی مجاز است."
        return context


class FileErrorOligo(TemplateView):
    template_name = "temporary/show_text.html"

    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['text'] = "در ستون " + \
                          "Primer Sequence (5 to 3)" + \
                          " تنها مقادیر" + "ACGTNRYSWKMBDHV" + " مجاز است."
        return context


class FileErrorIncomplete(TemplateView):
    template_name = "temporary/show_text.html"

    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['text'] = "فایل شامل سطر هایی ناقص است." + \
                          " لطفا در تمام سطرهایی که اطلاعات پر می کنید، تمامی بخش ها را پر کنید."
        return context


class CheckData(LoginRequiredMixin, FormView):
    form_class = CheckDataForm
    template_name = "order_service/check_data.html"
    success_url = reverse_lazy("index:index")

    def dispatch(self, request, *args, **kwargs):
        try:
            int(self.kwargs['pk'])
        except:
            return render(request, "temporary/show_text.html", {'text': "سفارش مورد نظر یافت نشد"})
        if not OrderService.objects.filter(id=self.kwargs['pk']):
            return render(request, "temporary/show_text.html", {'text': "سفارش مورد نظر یافت نشد"})
        order = OrderService.objects.get(id=self.kwargs['pk'])
        if self.request.user.is_superuser:
            return render(request, "temporary/show_text.html", {'text': "ثبت سفارش مخصوص مشتریان است"})
        if order.customer.username != self.request.user.username:
            return render(request, "temporary/show_text.html", {'text': "سفارش مورد نظر یافت نشد"})
        if order.is_finished:
            return render(request, "temporary/show_text.html", {'text': "سفارش مورد نظر با موفقیت ثبت شده است"})
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
        order = OrderService.objects.get(id=self.kwargs['pk'])
        service = order.service
        context['service'] = service
        fields = service.field_names.split(';')[:-1]
        context['fields'] = fields
        content = order.file.read()
        book = xlrd.open_workbook(file_contents=content)
        sheet = book.sheet_by_index(0)
        row_index = 3
        data = []
        while row_index < sheet.nrows:
            row = []
            check = False
            for j in range(1, sheet.ncols):
                if sheet.cell_value(row_index, j):
                    row.append(sheet.cell_value(row_index, j))
                    check = True
            row_index += 1
            if check:
                data.append(row)
        context['data'] = data
        context['fields2'] = Field2.objects.all().order_by('id')
        return context

    def form_valid(self, form):
        order = OrderService.objects.get(id=self.kwargs['pk'])
        service = order.service
        customer = Customer.objects.get(username=self.request.user.username)
        all_orders = OrderService.objects.filter(date=jdatetime.datetime.now().date(), is_finished=True).order_by('id')
        index = len(all_orders)
        order.is_finished = True
        order.name = form.cleaned_data['name']
        code = service.name + "-" + str(jdatetime.datetime.now().date()) + "-" + str(index)
        order.code = code
        order.date = jdatetime.datetime.now()
        order.save()
        mail_text = "با سلام،\nکاربر با نام "
        if customer.is_person:
            mail_text += customer.first_name + " " + customer.last_name
        else:
            mail_text += customer.last_name
        mail_text += " و نام کاربری " + customer.username + " سفارش با شناسه " + order.code + "ثبت کرد. "
        mail_text += "برای مشاهده جزئیات، برروی لینک زیر کلیک کنید."
        mail_text += "\nhttp://www.royantucagene.com/admin_panel"
        send_mail('ثبت سفارش', mail_text, 'Royan TuCAGene', [RoyanTucagene.objects.all()[0].email])
        self.success_url = reverse_lazy('order_service:get_code', kwargs={'pk': order.id})
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
        if not OrderService.objects.filter(id=int(self.kwargs['pk'])):
            return render(request, "temporary/show_text.html", {'text': "سفارش مورد نظر یافت نشد"})
        if OrderService.objects.filter(id=int(self.kwargs['pk'])).customer.username != request.user.username:
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
        order = OrderService.objects.filter(id=int(self.kwargs['pk']))
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
        mail_text += "و نام کاربری " + self.request.user.username + "سفارش با شناسه " + order.code + \
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
