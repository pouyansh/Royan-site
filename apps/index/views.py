from django.urls import reverse_lazy
from django.views.generic import CreateView, TemplateView

from apps.news.forms import *
from apps.news.models import *


class Index(TemplateView):
    template_name = 'index/index.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        news = News.objects.all()
        context['news'] = reversed(news[len(news)-4:len(news)])
        context['products'] = []
        return context

