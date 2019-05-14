from django.views.generic import TemplateView

from apps.news.models import *
from apps.product.models import Category, Product
from apps.research.models import ResearchArea
from apps.royan_admin.models import RoyanTucagene
from apps.service.models import Service, Field
from apps.tutorial.models import Tutorial


class Index(TemplateView):
    template_name = 'index/index.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['RoyanTucagene'] = RoyanTucagene.objects.all()[0]
        news = News.objects.all()
        context['news'] = reversed(news[max(0, len(news) - 4):len(news)])
        products = Product.objects.filter(is_active=True)
        if len(products) >= 2:
            context['product1'] = products[len(products) - 1]
            context['product2'] = products[len(products) - 2]
        if len(products) == 1:
            context['product1'] = products[len(products) - 1]
            context['product2'] = None
        if len(products) == 0:
            context['product1'] = None
            context['product2'] = None
        context['product_categories'] = Category.objects.filter(is_active=True).order_by('id')
        context['services'] = Service.objects.all().order_by('id')
        context['service_fields'] = Field.objects.all().order_by('id')
        context['research_areas'] = ResearchArea.objects.all().order_by('id')
        context['tutorials'] = Tutorial.objects.all().order_by('id')
        return context


class About(TemplateView):
    template_name = "index/about.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['RoyanTucagene'] = RoyanTucagene.objects.all()[0]
        context['product_categories'] = Category.objects.filter(is_active=True).order_by('id')
        context['services'] = Service.objects.all().order_by('id')
        context['service_fields'] = Field.objects.all().order_by('id')
        context['research_areas'] = ResearchArea.objects.all().order_by('id')
        context['tutorials'] = Tutorial.objects.all().order_by('id')
        return context
