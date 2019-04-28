import csv

from django.urls import reverse_lazy
from django.views.generic import FormView

from apps.order.forms import *
from apps.order.models import Order
from apps.product.models import Category
from apps.registration.models import Person, Organization, Customer
from apps.research.models import ResearchArea
from apps.service.models import Service, Field
from apps.tutorial.models import Tutorial


class SubmitOrderService(FormView):
    form_class = OrderServiceFrom
    template_name = 'order/order_service.html'
    success_url = reverse_lazy('index:index')

    # TODO check for admin and service existence

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
            orders = Order.objects.filter(customer=customer, service=service, is_finished=False)
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
            if row[1] == "text":
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
        order_id = form.cleaned_data['order_id']
        service = Service.objects.get(id=self.kwargs['pk'])
        if not self.request.user.is_superuser:
            customer = Customer.objects.get(username=self.request.user.username)
            orders = Order.objects.filter(customer=customer, service=service, is_finished=False)
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
            order = Order(customer=customer, service=service)
            order.save()
            content_data = []
        try:
            if order_id != -1:
                print(order_id)
                with open(order.file.path, 'w+') as f:
                    f.truncate()
                    writer = csv.writer(f)
                    for i in range(len(content_data)):
                        if i != order_id-1:
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
        self.success_url = reverse_lazy('order:order_service', kwargs={'pk': self.kwargs['pk']})
        return super(SubmitOrderService, self).form_valid(form)

    def form_invalid(self, form):
        print("invalid")
        return super(SubmitOrderService, self).form_invalid(form)
