from django.views.generic import TemplateView

from apps.product.models import Category
from apps.research.models import ResearchArea
from apps.service.models import *
from apps.tutorial.models import Tutorial


class AdminPanel(TemplateView):
    template_name = 'royan_admin/admin_panel.html'

    def get_context_data(self, **kwargs):
        context = super(AdminPanel, self).get_context_data()
        context['product_categories'] = Category.objects.all().order_by('id')
        context['admin'] = self.request.user
        context['services'] = Service.objects.all().order_by('id')
        context['service_fields'] = Field.objects.all().order_by('id')
        context['research_areas'] = ResearchArea.objects.all().order_by('id')
        context['tutorials'] = Tutorial.objects.all().order_by('id')
        return context

