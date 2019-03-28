from django.views.generic import TemplateView

from apps.news.models import *
from apps.product.models import Category, Product
from apps.service.models import Service, Field


class Index(TemplateView):
    template_name = 'index/index.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        news = News.objects.all()
        context['news'] = reversed(news[max(0, len(news) - 4):len(news)])
        products = Product.objects.filter(is_available=True)
        if len(products) >= 2:
            context['product1'] = products[len(products) - 1]
            context['product2'] = products[len(products) - 2]
        if len(products) == 1:
            context['product1'] = products[len(products) - 1]
            context['product2'] = None
        if len(products) == 0:
            context['product1'] = None
            context['product2'] = None
        context['product_categories'] = Category.objects.all()
        context['services'] = Service.objects.all()
        context['service_fields'] = Field.objects.all()
        return context
