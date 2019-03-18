from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import CreateView, DetailView

from apps.index.forms import *
from apps.index.models import *


def index(request):
    return render(request, 'index/index.html')


class Index(DetailView):
    template_name = 'index/index.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['news'] = News.objects.all()[:4]
        return context


class AddNews(CreateView):
    model = News
    template_name = 'index/add_news.html'

    form_class = AddNewsForm
    success_url = reverse_lazy('index:index')

    def get_queryset(self):
        return super(AddNews, self).get_queryset()
