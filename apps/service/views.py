from django.urls import reverse_lazy
from django.views.generic import CreateView

from apps.product.models import Category
from apps.service.forms import *
from apps.service.models import *


class CreateField(CreateView):
    model = Field
    template_name = 'service/create_field.html'
    success_url = reverse_lazy('index:index')
    form_class = CreateFieldForm

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['product_categories'] = Category.objects.all()
        return context


class CreateService(CreateView):
    model = Service
    template_name = 'service/create_service.html'
    success_url = reverse_lazy('index:index')
    form_class = CreateServiceForm

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['product_categories'] = Category.objects.all()
        context['fields'] = Field.objects.all()
        return context

    def form_valid(self, form):
        form.instance.field = Field.objects.get(id=form.cleaned_data['field'])
        return super(CreateService, self).form_valid(form)
