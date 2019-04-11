from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.views.generic import CreateView, ListView, FormView, UpdateView, TemplateView, DetailView

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
        context['services'] = Service.objects.all()
        context['service_fields'] = Field.objects.all()
        return context


class ShowFieldListAdmin(ListView, FormView):
    model = Field
    template_name = 'service/show_field_list_admin.html'

    success_url = reverse_lazy('service:delete_field_successful')
    form_class = FieldListAdminForm

    def form_valid(self, form):
        field = Field.objects.filter(id=form.cleaned_data['field_id'])
        services = Service.objects.filter(field=field[0])
        if services:
            self.success_url = reverse_lazy('service:delete_field_unsuccessful')
        else:
            Field.objects.filter(id=form.cleaned_data['field_id']).delete()
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['product_categories'] = Category.objects.all()
        context['services'] = Service.objects.all()
        context['service_fields'] = Field.objects.all()
        context['fields'] = Field.objects.all()
        return context


class DeleteFieldSuccessful(TemplateView):
    template_name = 'temporary/show_text.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['product_categories'] = Category.objects.all()
        context['services'] = Service.objects.all()
        context['service_fields'] = Field.objects.all()
        context['text'] = "زمینه مدنظر شما با موفقیت پاک شد"
        return context


class DeleteFieldUnsuccessful(TemplateView):
    template_name = 'temporary/show_text.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['product_categories'] = Category.objects.all()
        context['services'] = Service.objects.all()
        context['service_fields'] = Field.objects.all()
        context['text'] = "متاسفانه سرویسی در این فیلد وجود دارد و امکان حذف این فیلد وجود ندارد"
        return context


class UpdateField(UpdateView):
    model = Field
    template_name = 'service/update_field.html'
    success_url = reverse_lazy('service:show_field_list_admin')
    form_class = CreateFieldForm

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['product_categories'] = Category.objects.all()
        context['services'] = Service.objects.all()
        context['service_fields'] = Field.objects.all()
        return context


class ProductDetails(DetailView):
    model = Field
    template_name = 'service/field_details.html'

    def dispatch(self, request, *args, **kwargs):
        if not Field.objects.filter(id=self.kwargs['pk']):
            return redirect('index:index')
        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        product = Field.objects.filter(id=self.kwargs['pk'])
        if product:
            products = Field.objects.filter(category=product[0].category).exclude(name=product[0].name)
            if len(products) > 4:
                products = products[:4]
            context['related_products'] = products
        else:
            context['related_products'] = []
        context['product_categories'] = Category.objects.all()
        context['services'] = Service.objects.all()
        context['service_fields'] = Field.objects.all()
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
        context['services'] = Service.objects.all()
        context['service_fields'] = Field.objects.all()
        return context

    def form_valid(self, form):
        form.instance.field = Field.objects.get(id=form.cleaned_data['field'])
        return super(CreateService, self).form_valid(form)
