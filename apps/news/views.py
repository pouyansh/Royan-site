from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.views.generic import CreateView, DetailView, ListView, UpdateView, FormView

from apps.news.forms import *
from apps.news.models import News
from apps.product.models import Category
from apps.research.models import ResearchArea
from apps.service.models import Service, Field


class AddNews(CreateView):
    model = News
    template_name = 'news/add_news.html'

    form_class = AddNewsForm
    success_url = reverse_lazy('index:index')

    def get_queryset(self):
        return super(AddNews, self).get_queryset()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['product_categories'] = Category.objects.all().order_by('id')
        context['services'] = Service.objects.all().order_by('id')
        context['service_fields'] = Field.objects.all().order_by('id')
        context['research_areas'] = ResearchArea.objects.all().order_by('id')
        return context


class UpdateNews(UpdateView):
    model = News
    template_name = 'news/update_news.html'
    form_class = UpdateNewsForm
    success_url = reverse_lazy('index:index')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['product_categories'] = Category.objects.all().order_by('id')
        context['services'] = Service.objects.all().order_by('id')
        context['service_fields'] = Field.objects.all().order_by('id')
        context['research_areas'] = ResearchArea.objects.all().order_by('id')
        return context


class ShowNewsDetail(DetailView):
    model = News
    template_name = 'news/show_news.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['product_categories'] = Category.objects.all().order_by('id')
        context['services'] = Service.objects.all().order_by('id')
        context['service_fields'] = Field.objects.all().order_by('id')
        context['research_areas'] = ResearchArea.objects.all().order_by('id')
        return context

    def dispatch(self, request, *args, **kwargs):
        if not News.objects.filter(id=self.kwargs['pk']):
            return redirect('index:index')
        return super().dispatch(request, *args, **kwargs)


class ShowNewsList(ListView):
    model = News
    template_name = 'news/show_news_list.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['product_categories'] = Category.objects.all().order_by('id')
        context['services'] = Service.objects.all().order_by('id')
        context['service_fields'] = Field.objects.all().order_by('id')
        context['research_areas'] = ResearchArea.objects.all().order_by('id')
        return context


class ShowNewsListAdmin(ListView, FormView):
    model = News
    template_name = 'news/show_news_list_admin.html'

    success_url = reverse_lazy('news:show_news_list_admin')
    form_class = NewsListAdminForm

    def form_valid(self, form):
        News.objects.filter(id=form.cleaned_data['news_id']).delete()
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['product_categories'] = Category.objects.all().order_by('id')
        context['services'] = Service.objects.all().order_by('id')
        context['service_fields'] = Field.objects.all().order_by('id')
        context['research_areas'] = ResearchArea.objects.all().order_by('id')
        return context
