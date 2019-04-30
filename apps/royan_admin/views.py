from django.views.generic import TemplateView

from apps.order_service.models import OrderService
from apps.product.models import Category
from apps.research.models import ResearchArea
from apps.service.models import *
from apps.tutorial.models import Tutorial


class AdminPanel(TemplateView):
    template_name = 'royan_admin/admin_panel.html'

    def get_context_data(self, **kwargs):
        context = super(AdminPanel, self).get_context_data()
        context['product_categories'] = Category.objects.filter(is_active=True).order_by('id')
        context['admin'] = self.request.user
        context['services'] = Service.objects.all().order_by('id')
        context['service_fields'] = Field.objects.all().order_by('id')
        context['research_areas'] = ResearchArea.objects.all().order_by('id')
        context['tutorials'] = Tutorial.objects.all().order_by('id')
        context['finished_orders'] = OrderService.objects.filter(is_finished=True, invoice=True, received=True,
                                                                 payed=True)
        context['orders_not_payment'] = OrderService.objects.filter(is_finished=True, invoice=True, payed=False)
        context['orders_not_received'] = OrderService.objects.filter(is_finished=True, invoice=True, received=False)
        context['orders_not_invoice'] = OrderService.objects.filter(is_finished=True, invoice=False)
        context['orders_not_finished'] = OrderService.objects.filter(is_finished=False)
        return context
