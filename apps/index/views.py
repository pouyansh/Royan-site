from django.urls import reverse_lazy
from django.views.generic import CreateView, TemplateView

from apps.index.forms import *
from apps.index.models import *


class Index(TemplateView):
    template_name = 'index/index.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        news = News.objects.all()
        context['news'] = reversed(news[len(news)-4:len(news)])
        context['products'] = []
        return context


class AddNews(CreateView):
    model = News
    template_name = 'index/add_news.html'

    form_class = AddNewsForm
    success_url = reverse_lazy('index:index')

    def get_queryset(self):
        return super(AddNews, self).get_queryset()
