import csv
import os

from django.core.files.base import ContentFile
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.views.generic import CreateView, ListView, FormView, UpdateView, TemplateView, DetailView

from apps.product.models import Category
from apps.research.models import ResearchArea
from apps.royan_admin.models import RoyanTucagene
from apps.service.forms import *
from apps.service.models import *
from apps.tutorial.models import Tutorial


class CreateField(CreateView):
    model = Field
    template_name = 'service/create_field.html'
    success_url = reverse_lazy('index:index')
    form_class = CreateFieldForm

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['RoyanTucagene'] = RoyanTucagene.objects.all()[0]
        context['product_categories'] = Category.objects.filter(is_active=True).order_by('id')
        context['services'] = Service.objects.all().order_by('id')
        context['service_fields'] = Field.objects.all().order_by('id')
        context['research_areas'] = ResearchArea.objects.all().order_by('id')
        context['tutorials'] = Tutorial.objects.all().order_by('id')
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
        context['RoyanTucagene'] = RoyanTucagene.objects.all()[0]
        context['product_categories'] = Category.objects.filter(is_active=True).order_by('id')
        context['services'] = Service.objects.all().order_by('id')
        context['service_fields'] = Field.objects.all().order_by('id')
        context['fields'] = Field.objects.all().order_by('id')
        context['research_areas'] = ResearchArea.objects.all().order_by('id')
        context['tutorials'] = Tutorial.objects.all().order_by('id')
        return context


class DeleteFieldSuccessful(TemplateView):
    template_name = 'temporary/show_text.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['RoyanTucagene'] = RoyanTucagene.objects.all()[0]
        context['product_categories'] = Category.objects.filter(is_active=True).order_by('id')
        context['services'] = Service.objects.all().order_by('id')
        context['service_fields'] = Field.objects.all().order_by('id')
        context['research_areas'] = ResearchArea.objects.all().order_by('id')
        context['tutorials'] = Tutorial.objects.all().order_by('id')
        context['text'] = "زمینه مدنظر شما با موفقیت پاک شد"
        return context


class DeleteFieldUnsuccessful(TemplateView):
    template_name = 'temporary/show_text.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['RoyanTucagene'] = RoyanTucagene.objects.all()[0]
        context['product_categories'] = Category.objects.filter(is_active=True).order_by('id')
        context['services'] = Service.objects.all().order_by('id')
        context['service_fields'] = Field.objects.all().order_by('id')
        context['research_areas'] = ResearchArea.objects.all().order_by('id')
        context['tutorials'] = Tutorial.objects.all().order_by('id')
        context['text'] = "متاسفانه سرویسی در این فیلد وجود دارد و امکان حذف این فیلد وجود ندارد"
        return context


class UpdateField(UpdateView):
    model = Field
    template_name = 'service/update_field.html'
    success_url = reverse_lazy('service:show_field_list_admin')
    form_class = CreateFieldForm

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['RoyanTucagene'] = RoyanTucagene.objects.all()[0]
        context['product_categories'] = Category.objects.filter(is_active=True).order_by('id')
        context['services'] = Service.objects.all().order_by('id')
        context['service_fields'] = Field.objects.all().order_by('id')
        context['research_areas'] = ResearchArea.objects.all().order_by('id')
        context['tutorials'] = Tutorial.objects.all().order_by('id')
        return context


class FieldDetails(DetailView):
    model = Field
    template_name = 'service/field_details.html'

    def dispatch(self, request, *args, **kwargs):
        if not Field.objects.filter(id=self.kwargs['pk']):
            return redirect('index:index')
        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        field = Field.objects.filter(id=self.kwargs['pk'])
        if field:
            services = Service.objects.filter(field=field[0])
            if len(services) > 4:
                services = services[:4]
            context['related_services'] = services
        else:
            context['related_services'] = []

        context['RoyanTucagene'] = RoyanTucagene.objects.all()[0]
        context['product_categories'] = Category.objects.filter(is_active=True).order_by('id')
        context['services'] = Service.objects.all().order_by('id')
        context['service_fields'] = Field.objects.all().order_by('id')
        context['research_areas'] = ResearchArea.objects.all().order_by('id')
        context['tutorials'] = Tutorial.objects.all().order_by('id')
        return context


class CreateField2(CreateView):
    model = Field2
    template_name = 'service/create_field2.html'
    success_url = reverse_lazy('index:index')
    form_class = CreateField2Form

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['RoyanTucagene'] = RoyanTucagene.objects.all()[0]
        context['product_categories'] = Category.objects.filter(is_active=True).order_by('id')
        context['fields'] = Field.objects.all().order_by('id')
        context['services'] = Service.objects.all().order_by('id')
        context['service_fields'] = Field.objects.all().order_by('id')
        context['research_areas'] = ResearchArea.objects.all().order_by('id')
        context['tutorials'] = Tutorial.objects.all().order_by('id')
        return context

    def form_valid(self, form):
        field_id = form.cleaned_data['field']
        form.instance.field = Field.objects.get(id=field_id)
        return super(CreateField2, self).form_valid(form)


class ShowField2ListAdmin(ListView, FormView):
    model = Field2
    template_name = 'service/show_field2_list_admin.html'

    success_url = reverse_lazy('service:delete_field_successful')
    form_class = FieldListAdminForm

    def form_valid(self, form):
        field = Field2.objects.filter(id=form.cleaned_data['field_id'])
        services = Service.objects.filter(field2=field[0])
        if services:
            self.success_url = reverse_lazy('service:delete_field_unsuccessful')
        else:
            Field2.objects.filter(id=form.cleaned_data['field_id']).delete()
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['RoyanTucagene'] = RoyanTucagene.objects.all()[0]
        context['product_categories'] = Category.objects.filter(is_active=True).order_by('id')
        context['services'] = Service.objects.all().order_by('id')
        context['service_fields'] = Field.objects.all().order_by('id')
        context['fields'] = Field2.objects.all().order_by('id')
        context['research_areas'] = ResearchArea.objects.all().order_by('id')
        context['tutorials'] = Tutorial.objects.all().order_by('id')
        return context


class UpdateField2(UpdateView):
    model = Field2
    template_name = 'service/update_field.html'
    success_url = reverse_lazy('service:show_field_list_admin')
    form_class = CreateField2Form

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['RoyanTucagene'] = RoyanTucagene.objects.all()[0]
        context['product_categories'] = Category.objects.filter(is_active=True).order_by('id')
        context['services'] = Service.objects.all().order_by('id')
        context['service_fields'] = Field.objects.all().order_by('id')
        context['research_areas'] = ResearchArea.objects.all().order_by('id')
        context['tutorials'] = Tutorial.objects.all().order_by('id')
        return context


class CreateService(CreateView):
    model = Service
    template_name = 'service/create_service.html'
    success_url = reverse_lazy('index:index')
    form_class = CreateServiceForm

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['RoyanTucagene'] = RoyanTucagene.objects.all()[0]
        context['product_categories'] = Category.objects.filter(is_active=True).order_by('id')
        context['fields'] = Field.objects.all().order_by('id')
        context['fields2'] = Field2.objects.all().order_by('id')
        context['services'] = Service.objects.all().order_by('id')
        context['service_fields'] = Field.objects.all().order_by('id')
        context['research_areas'] = ResearchArea.objects.all().order_by('id')
        context['tutorials'] = Tutorial.objects.all().order_by('id')
        return context

    def form_valid(self, form):
        field_id = form.cleaned_data['field']
        ids = field_id.split('-')
        form.instance.field = Field.objects.get(id=ids[0])
        form.instance.field2 = Field2.objects.get(id=ids[1])
        return super(CreateService, self).form_valid(form)


class ServiceDetails(DetailView):
    model = Service
    template_name = 'service/service_details.html'

    def dispatch(self, request, *args, **kwargs):
        if not Service.objects.filter(id=self.kwargs['pk']):
            return redirect('index:index')
        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['RoyanTucagene'] = RoyanTucagene.objects.all()[0]
        service = Service.objects.filter(id=self.kwargs['pk'])
        if service:
            context['field'] = service[0].field
            services = Service.objects.filter(field=service[0].field).exclude(name=service[0].name)
            if len(services) > 4:
                services = services[:4]
            context['related_services'] = services
        else:
            context['related_services'] = []
        context['product_categories'] = Category.objects.filter(is_active=True).order_by('id')
        context['services'] = Service.objects.all().order_by('id')
        context['service_fields'] = Field.objects.all().order_by('id')
        context['research_areas'] = ResearchArea.objects.all().order_by('id')
        context['tutorials'] = Tutorial.objects.all().order_by('id')
        return context


class ShowServiceListAdmin(ListView, FormView):
    model = Service
    template_name = 'service/show_service_list_admin.html'

    success_url = reverse_lazy('service:delete_service_successful')
    form_class = ServiceListAdminForm

    def form_valid(self, form):
        Service.objects.filter(id=form.cleaned_data['service_id']).delete()
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['RoyanTucagene'] = RoyanTucagene.objects.all()[0]
        context['product_categories'] = Category.objects.filter(is_active=True).order_by('id')
        context['services'] = Service.objects.all().order_by('id')
        context['service_fields'] = Field.objects.all().order_by('id')
        context['research_areas'] = ResearchArea.objects.all().order_by('id')
        context['tutorials'] = Tutorial.objects.all().order_by('id')
        return context


class DeleteServiceSuccessful(TemplateView):
    template_name = 'temporary/show_text.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['RoyanTucagene'] = RoyanTucagene.objects.all()[0]
        context['product_categories'] = Category.objects.filter(is_active=True).order_by('id')
        context['services'] = Service.objects.all().order_by('id')
        context['service_fields'] = Field.objects.all().order_by('id')
        context['research_areas'] = ResearchArea.objects.all().order_by('id')
        context['tutorials'] = Tutorial.objects.all().order_by('id')
        context['text'] = "سرویس مدنظر شما با موفقیت پاک شد"
        return context


class UpdateService(UpdateView):
    model = Service
    template_name = 'service/update_service.html'
    success_url = reverse_lazy('service:show_service_list_admin')
    form_class = UpdateServiceForm

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['RoyanTucagene'] = RoyanTucagene.objects.all()[0]
        context['product_categories'] = Category.objects.filter(is_active=True).order_by('id')
        context['services'] = Service.objects.all().order_by('id')
        context['service_fields'] = Field.objects.all().order_by('id')
        context['research_areas'] = ResearchArea.objects.all().order_by('id')
        context['tutorials'] = Tutorial.objects.all().order_by('id')
        return context

    def form_valid(self, form):
        field_id = form.cleaned_data['field']
        if str(field_id) != "-1":
            ids = field_id.split('-')
            form.instance.field = Field.objects.get(id=ids[0])
            form.instance.field2 = Field2.objects.get(id=ids[1])
        return super(UpdateService, self).form_valid(form)


class CreateFormForService(FormView):
    template_name = "service/create_form.html"
    form_class = CreateFormForm
    success_url = reverse_lazy("index:index")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['RoyanTucagene'] = RoyanTucagene.objects.all()[0]
        context['product_categories'] = Category.objects.filter(is_active=True).order_by('id')
        context['services'] = Service.objects.all().order_by('id')
        context['service_fields'] = Field.objects.all().order_by('id')
        context['research_areas'] = ResearchArea.objects.all().order_by('id')
        context['tutorials'] = Tutorial.objects.all().order_by('id')
        service = Service.objects.get(id=self.kwargs['pk'])
        context['service'] = service
        if not service.fields:
            if not os.path.exists("services/"):
                os.mkdir("services/")
            if not os.path.exists("services/service_" + str(service.id)):
                os.mkdir("services/service_" + str(service.id))
            f = open("services/service_" + str(service.id) + "/fields.csv", "x")
            f.close()
            service.fields.save("services/service_" + str(service.id) + "/fields.csv", ContentFile(''), save=True)
        with open(service.fields.path, 'r') as f:
            fields_file = csv.reader(f)
            fields = []
            for row in fields_file:
                fields.append(row)
            context['fields'] = fields
        return context

    def form_valid(self, form):
        service = Service.objects.get(id=self.kwargs['pk'])
        if form.cleaned_data['file']:
            service.file = form.cleaned_data['file']
            service.save()
        if str(form.cleaned_data['final']) == "1":
            service.has_form = True
            service.save()
        elif str(form.cleaned_data['final']) == "2":
            service.has_form = False
            service.save()
        else:
            if str(form.cleaned_data['field_id']) != "-1":
                with open(service.fields.path, 'r') as f:
                    fields_file = csv.reader(f)
                    fields = []
                    for row in fields_file:
                        fields.append(row)
                new_fields = []
                for i in range(len(fields)):
                    if i + 1 != int(form.cleaned_data['field_id']):
                        new_fields.append(fields[i])
                with open(service.fields.path, 'w') as f:
                    fields_file = csv.writer(f)
                    for row in new_fields:
                        fields_file.writerow(row)
            else:
                row = [form.cleaned_data['name'], form.cleaned_data['type'], form.cleaned_data['name']]
                print(form.cleaned_data['type'])
                if form.cleaned_data['type'] == "text" or form.cleaned_data['type'] == "oligo":
                    row.append(form.cleaned_data['description'])
                if form.cleaned_data['type'] == "choice":
                    choices = form.cleaned_data['description'].split(',')
                    for choice in choices:
                        row.append(choice)
                with open(service.fields.path, 'a') as f:
                    fields_file = csv.writer(f)
                    fields_file.writerow(row)
            self.success_url = reverse_lazy("service:create_form", kwargs={'pk': self.kwargs['pk']})
        return super(CreateFormForService, self).form_valid(form)
