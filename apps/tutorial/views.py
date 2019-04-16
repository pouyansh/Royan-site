from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.views.generic import CreateView, UpdateView, DetailView, ListView, FormView

from apps.product.models import Category
from apps.research.models import ResearchArea
from apps.service.models import *
from apps.tutorial.forms import *
from apps.tutorial.models import Tutorial, Paper


class AddTutorial(CreateView):
    model = Tutorial
    template_name = 'tutorial/add_tutorial.html'

    form_class = AddTutorialForm
    success_url = reverse_lazy('index:index')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['product_categories'] = Category.objects.all().order_by('id')
        context['services'] = Service.objects.all().order_by('id')
        context['service_fields'] = Field.objects.all().order_by('id')
        context['research_areas'] = ResearchArea.objects.all().order_by('id')
        return context


class UpdateTutorial(UpdateView):
    model = Tutorial
    template_name = 'tutorial/update_tutorial.html'
    form_class = AddTutorialForm
    success_url = reverse_lazy('tutorial:show_tutorial_list_admin')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['product_categories'] = Category.objects.all().order_by('id')
        context['services'] = Service.objects.all().order_by('id')
        context['service_fields'] = Field.objects.all().order_by('id')
        context['research_areas'] = ResearchArea.objects.all().order_by('id')
        return context


class ShowTutorialDetail(DetailView):
    model = Tutorial
    template_name = 'tutorial/show_tutorial.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['product_categories'] = Category.objects.all().order_by('id')
        context['services'] = Service.objects.all().order_by('id')
        context['service_fields'] = Field.objects.all().order_by('id')
        context['research_areas'] = ResearchArea.objects.all().order_by('id')
        tutorial = Tutorial.objects.get(id=self.kwargs['pk'])
        context['tutorial'] = tutorial
        context['related_papers'] = Paper.objects.filter(tutorial=tutorial)
        return context

    def dispatch(self, request, *args, **kwargs):
        if not Tutorial.objects.filter(id=self.kwargs['pk']):
            return redirect('index:index')
        return super().dispatch(request, *args, **kwargs)


class ShowResearchAreaListAdmin(ListView, FormView):
    model = Tutorial
    template_name = 'tutorial/show_tutorial_list_admin.html'

    success_url = reverse_lazy('tutorial:show_tutorial_list_admin')
    form_class = TutorialListAdminForm

    def form_valid(self, form):
        Tutorial.objects.filter(id=form.cleaned_data['tutorial_id']).delete()
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['product_categories'] = Category.objects.all().order_by('id')
        context['services'] = Service.objects.all().order_by('id')
        context['service_fields'] = Field.objects.all().order_by('id')
        context['research_areas'] = ResearchArea.objects.all().order_by('id')
        context['tutorials'] = Tutorial.objects.all().order_by('id')
        return context


