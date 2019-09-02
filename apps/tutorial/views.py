from django.shortcuts import redirect, get_object_or_404
from django.urls import reverse_lazy
from django.views.generic import CreateView, UpdateView, DetailView, ListView, FormView

from apps.product.models import Category
from apps.research.models import ResearchArea
from apps.royan_admin.models import RoyanTucagene
from apps.service.models import *
from apps.tutorial.forms import *
from apps.tutorial.models import *


class AddTutorial(CreateView):
    model = Tutorial
    template_name = 'tutorial/add_tutorial.html'

    form_class = AddTutorialForm
    success_url = reverse_lazy('index:index')

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


class UpdateTutorial(UpdateView):
    model = Tutorial
    template_name = 'tutorial/update_tutorial.html'
    form_class = AddTutorialForm
    success_url = reverse_lazy('tutorial:show_tutorial_list_admin')

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


class ShowTutorialDetail(DetailView):
    model = Tutorial
    template_name = 'tutorial/show_tutorial.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['RoyanTucagene'] = RoyanTucagene.objects.all()[0]
        context['product_categories'] = Category.objects.filter(is_active=True).order_by('id')
        context['services'] = Service.objects.all().order_by('id')
        context['service_fields'] = Field.objects.all().order_by('id')
        context['research_areas'] = ResearchArea.objects.all().order_by('id')
        context['tutorials'] = Tutorial.objects.all().order_by('id')
        context['fields2'] = Field2.objects.all().order_by('id')
        tutorial = Tutorial.objects.get(id=self.kwargs['pk'])
        context['tutorial'] = tutorial
        context['links'] = Links.objects.filter(tutorial=tutorial).order_by('rank')
        return context

    def dispatch(self, request, *args, **kwargs):
        if not Tutorial.objects.filter(id=self.kwargs['pk']):
            return redirect('index:index')
        return super().dispatch(request, *args, **kwargs)


class ShowTutorialListAdmin(ListView, FormView):
    model = Tutorial
    template_name = 'tutorial/show_tutorial_list_admin.html'

    success_url = reverse_lazy('tutorial:show_tutorial_list_admin')
    form_class = TutorialListAdminForm

    def form_valid(self, form):
        Tutorial.objects.filter(id=form.cleaned_data['tutorial_id']).delete()
        return super().form_valid(form)

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


class ChooseTutorial(ListView):
    model = Tutorial
    template_name = 'tutorial/choose_tutorial.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['RoyanTucagene'] = RoyanTucagene.objects.all()[0]
        context['product_categories'] = Category.objects.filter(is_active=True).order_by('id')
        context['services'] = Service.objects.all().order_by('id')
        context['service_fields'] = Field.objects.all().order_by('id')
        context['fields2'] = Field2.objects.all().order_by('id')
        context['research_areas'] = ResearchArea.objects.all().order_by('id')
        context['tutorials'] = Tutorial.objects.all().order_by('id')
        return context


class CreateLink(CreateView):
    model = Links
    form_class = AddLinkForm
    template_name = 'tutorial/create_link.html'
    success_url = reverse_lazy('tutorial:show_tutorial_list_admin')

    def dispatch(self, request, *args, **kwargs):
        if not Tutorial.objects.filter(id=self.kwargs['pk']):
            return redirect('index:index')
        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['RoyanTucagene'] = RoyanTucagene.objects.all()[0]
        context['product_categories'] = Category.objects.filter(is_active=True).order_by('id')
        context['services'] = Service.objects.all().order_by('id')
        context['service_fields'] = Field.objects.all().order_by('id')
        context['fields2'] = Field2.objects.all().order_by('id')
        context['research_areas'] = ResearchArea.objects.all().order_by('id')
        context['tutorials'] = Tutorial.objects.all().order_by('id')
        context['tutorial'] = Tutorial.objects.get(id=self.kwargs['pk'])
        return context

    def form_valid(self, form):
        tutorial = get_object_or_404(Tutorial, pk=self.kwargs['pk'])
        form.instance.tutorial = tutorial
        return super().form_valid(form)


class UpdateLink(UpdateView):
    model = Links
    template_name = 'tutorial/update_link.html'
    form_class = AddLinkForm
    success_url = reverse_lazy('tutorial:show_tutorial_list_admin')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['RoyanTucagene'] = RoyanTucagene.objects.all()[0]
        context['product_categories'] = Category.objects.filter(is_active=True).order_by('id')
        context['services'] = Service.objects.all().order_by('id')
        context['service_fields'] = Field.objects.all().order_by('id')
        context['fields2'] = Field2.objects.all().order_by('id')
        context['research_areas'] = ResearchArea.objects.all().order_by('id')
        context['tutorials'] = Tutorial.objects.all().order_by('id')
        context['tutorial'] = Tutorial.objects.get(id=Links.objects.get(id=self.kwargs['pk']).tutorial.id)
        return context

    def dispatch(self, request, *args, **kwargs):
        if not Links.objects.filter(id=self.kwargs['pk']):
            return redirect('index:index')
        return super().dispatch(request, *args, **kwargs)


class ShowLink(DetailView):
    model = Links
    template_name = 'tutorial/show_link.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['RoyanTucagene'] = RoyanTucagene.objects.all()[0]
        context['product_categories'] = Category.objects.filter(is_active=True).order_by('id')
        context['services'] = Service.objects.all().order_by('id')
        context['service_fields'] = Field.objects.all().order_by('id')
        context['research_areas'] = ResearchArea.objects.all().order_by('id')
        context['tutorials'] = Tutorial.objects.all().order_by('id')
        context['fields2'] = Field2.objects.all().order_by('id')
        context['link'] = Links.objects.get(id=self.kwargs['pk'])
        return context

    def dispatch(self, request, *args, **kwargs):
        if not Links.objects.get(id=self.kwargs['pk']):
            return redirect('index:index')
        return super().dispatch(request, *args, **kwargs)
