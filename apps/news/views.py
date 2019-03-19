from django.urls import reverse_lazy
from django.views.generic import CreateView, DetailView, ListView, UpdateView, FormView

from apps.news.forms import *
from apps.news.models import News


class AddNews(CreateView):
    model = News
    template_name = 'news/add_news.html'

    form_class = AddNewsForm
    success_url = reverse_lazy('index:index')

    def get_queryset(self):
        return super(AddNews, self).get_queryset()


class UpdateNews(UpdateView):
    model = News
    template_name = 'news/update_news.html'
    form_class = UpdateNewsForm
    success_url = reverse_lazy('index:index')


class ShowNewsDetail(DetailView):
    model = News
    template_name = 'news/show_news.html'


class ShowNewsList(ListView):
    model = News
    template_name = 'news/show_news_list.html'


class ShowNewsListAdmin(ListView, FormView):
    model = News
    template_name = 'news/show_news_list_admin.html'

    success_url = reverse_lazy('news:show_news_list_admin')
    form_class = NewsListAdminForm

    def form_valid(self, form):
        print(form.cleaned_data['news_id'])
        News.objects.filter(id=form.cleaned_data['news_id']).delete()
        return super().form_valid(form)

