from django.shortcuts import redirect, get_object_or_404
from django.urls import reverse_lazy
from django.views.generic import CreateView, UpdateView, DetailView, ListView, FormView

from apps.product.models import Category
from apps.research.forms import *
from apps.research.models import ResearchArea, Paper
from apps.service.models import *
from apps.tutorial.models import Tutorial


class AddResearchArea(CreateView):
    model = ResearchArea
    template_name = 'research/add_research_area.html'

    form_class = AddResearchAreaForm
    success_url = reverse_lazy('index:index')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['product_categories'] = Category.objects.all().order_by('id')
        context['services'] = Service.objects.all().order_by('id')
        context['service_fields'] = Field.objects.all().order_by('id')
        context['research_areas'] = ResearchArea.objects.all().order_by('id')
        context['tutorials'] = Tutorial.objects.all().order_by('id')
        return context


class UpdateResearchArea(UpdateView):
    model = ResearchArea
    template_name = 'research/update_research_area.html'
    form_class = AddResearchAreaForm
    success_url = reverse_lazy('research:show_research_area_list_admin')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['product_categories'] = Category.objects.all().order_by('id')
        context['services'] = Service.objects.all().order_by('id')
        context['service_fields'] = Field.objects.all().order_by('id')
        context['research_areas'] = ResearchArea.objects.all().order_by('id')
        context['tutorials'] = Tutorial.objects.all().order_by('id')
        return context


class ShowResearchAreaDetail(DetailView):
    model = ResearchArea
    template_name = 'research/show_research_area.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['product_categories'] = Category.objects.all().order_by('id')
        context['services'] = Service.objects.all().order_by('id')
        context['service_fields'] = Field.objects.all().order_by('id')
        context['research_areas'] = ResearchArea.objects.all().order_by('id')
        context['tutorials'] = Tutorial.objects.all().order_by('id')
        research_area = ResearchArea.objects.get(id=self.kwargs['pk'])
        context['research_area'] = research_area
        context['related_papers'] = Paper.objects.filter(research_area=research_area)
        return context

    def dispatch(self, request, *args, **kwargs):
        if not ResearchArea.objects.filter(id=self.kwargs['pk']):
            return redirect('index:index')
        return super().dispatch(request, *args, **kwargs)


class ShowResearchAreaListAdmin(ListView, FormView):
    model = ResearchArea
    template_name = 'research/show_research_area_list_admin.html'

    success_url = reverse_lazy('research:show_research_area_list_admin')
    form_class = ResearchAreaListAdminForm

    def form_valid(self, form):
        ResearchArea.objects.filter(id=form.cleaned_data['research_area_id']).delete()
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['product_categories'] = Category.objects.all().order_by('id')
        context['services'] = Service.objects.all().order_by('id')
        context['service_fields'] = Field.objects.all().order_by('id')
        context['research_areas'] = ResearchArea.objects.all().order_by('id')
        context['tutorials'] = Tutorial.objects.all().order_by('id')
        return context


class CreatePaper(CreateView):
    model = Paper
    form_class = AddPaperForm
    template_name = 'research/create_paper.html'
    success_url = reverse_lazy('research:show_research_area_list_admin')

    def dispatch(self, request, *args, **kwargs):
        if not ResearchArea.objects.filter(id=self.kwargs['pk']):
            return redirect('index:index')
        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['product_categories'] = Category.objects.all().order_by('id')
        context['services'] = Service.objects.all().order_by('id')
        context['service_fields'] = Field.objects.all().order_by('id')
        context['research_areas'] = ResearchArea.objects.all().order_by('id')
        context['tutorials'] = Tutorial.objects.all().order_by('id')
        context['research_area'] = ResearchArea.objects.get(id=self.kwargs['pk'])
        return context

    def form_valid(self, form):
        research_area = get_object_or_404(ResearchArea, pk=self.kwargs['pk'])
        form.instance.research_area = research_area
        return super().form_valid(form)


class ShowPaperDetail(DetailView):
    model = Paper
    template_name = 'research/show_paper.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['product_categories'] = Category.objects.all().order_by('id')
        context['services'] = Service.objects.all().order_by('id')
        context['service_fields'] = Field.objects.all().order_by('id')
        context['research_areas'] = ResearchArea.objects.all().order_by('id')
        context['tutorials'] = Tutorial.objects.all().order_by('id')
        paper = Paper.objects.get(id=self.kwargs['pk'])
        context['related_papers'] = Paper.objects.filter(research_area=paper.research_area).exclude(title=paper.title)
        return context

    def dispatch(self, request, *args, **kwargs):
        if not Paper.objects.filter(id=self.kwargs['pk']):
            return redirect('index:index')
        return super().dispatch(request, *args, **kwargs)


class UpdatePaper(UpdateView):
    model = Paper
    template_name = 'research/update_paper.html'
    form_class = AddPaperForm
    success_url = reverse_lazy('research:show_research_area_list_admin')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['product_categories'] = Category.objects.all().order_by('id')
        context['services'] = Service.objects.all().order_by('id')
        context['service_fields'] = Field.objects.all().order_by('id')
        context['research_areas'] = ResearchArea.objects.all().order_by('id')
        context['tutorials'] = Tutorial.objects.all().order_by('id')
        return context
