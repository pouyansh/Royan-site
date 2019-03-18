from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import CreateView

from apps.index.models import *


def index(request):
    return render(request, 'index/index.html')


class AddNews(CreateView):
    model = News
    template_name = 'index/add_news.html'

    fields = ['title', 'summary', 'description', 'english_title', 'english_summary', 'english_description', 'image']
    success_url = reverse_lazy('index.index')

    def get_queryset(self):
        return super(AddNews, self).get_queryset()
