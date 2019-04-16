from django.urls import reverse_lazy
from django.views.generic import CreateView, UpdateView

from apps.product.models import Category
from apps.research.forms import AddResearchAreaForm
from apps.research.models import ResearchArea
from apps.service.models import *


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
        return context


class UpdateResearchArea(UpdateView):
    model = ResearchArea
    template_name = 'research/update_research_area.html'
    form_class = AddResearchAreaForm
    success_url = reverse_lazy('index:index')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['product_categories'] = Category.objects.all().order_by('id')
        context['services'] = Service.objects.all().order_by('id')
        context['service_fields'] = Field.objects.all().order_by('id')
        context['research_areas'] = ResearchArea.objects.all().order_by('id')
        return context
