from django.urls import reverse_lazy
from django.views.generic import CreateView

from apps.product.models import Category
from apps.research.models import ResearchArea
from apps.service.models import *
from apps.tutorial.forms import *
from apps.tutorial.models import Tutorial


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
