from django.urls import reverse_lazy
from django.views.generic import CreateView, DetailView

from apps.news.forms import AddNewsForm
from apps.news.models import News


class AddNews(CreateView):
    model = News
    template_name = 'news/add_news.html'

    form_class = AddNewsForm
    success_url = reverse_lazy('index:index')

    def get_queryset(self):
        return super(AddNews, self).get_queryset()


class ShowNewsDetail(DetailView):
    model = News
    template_name = 'news/show_news.html'
