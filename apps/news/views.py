from django.shortcuts import redirect, render
from django.urls import reverse_lazy
from django.views.generic import CreateView, DetailView, ListView, UpdateView, FormView, TemplateView

from apps.news.forms import *
from apps.news.models import News
from apps.product.models import Category
from apps.research.models import ResearchArea
from apps.service.models import Service, Field
from apps.tutorial.models import Tutorial


class AddNews(CreateView):
    model = News
    template_name = 'news/add_news.html'
    form_class = AddNewsForm
    success_url = reverse_lazy('index:index')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['product_categories'] = Category.objects.filter(is_active=True).order_by('id')
        context['services'] = Service.objects.all().order_by('id')
        context['service_fields'] = Field.objects.all().order_by('id')
        context['research_areas'] = ResearchArea.objects.all().order_by('id')
        context['tutorials'] = Tutorial.objects.all().order_by('id')
        return context


class UpdateNews(UpdateView):
    model = News
    template_name = 'news/update_news.html'
    form_class = UpdateNewsForm
    success_url = reverse_lazy('index:index')

    def dispatch(self, request, *args, **kwargs):
        try:
            int(self.kwargs['pk'])
            News.objects.get(id=self.kwargs['pk'])
        except:
            return render(request, "temporary/show_text.html", {'text': "خبر مورد نظر یافت نشد"})
        return super(UpdateNews, self).dispatch(request, args, kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['product_categories'] = Category.objects.filter(is_active=True).order_by('id')
        context['services'] = Service.objects.all().order_by('id')
        context['service_fields'] = Field.objects.all().order_by('id')
        context['research_areas'] = ResearchArea.objects.all().order_by('id')
        context['tutorials'] = Tutorial.objects.all().order_by('id')
        return context


class ShowNewsDetail(TemplateView):
    model = News
    template_name = 'news/show_news.html'

    def dispatch(self, request, *args, **kwargs):
        try:
            int(self.kwargs['pk'])
        except:
            return render(request, "temporary/show_text.html", {'text': "خبر مورد نظر یافت نشد"})
        if len(News.objects.all()) < int(self.kwargs['pk']):
            return render(request, "temporary/show_text.html", {'text': "خبر مورد نظر یافت نشد"})
        return super(ShowNewsDetail, self).dispatch(request, args, kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['product_categories'] = Category.objects.filter(is_active=True).order_by('id')
        context['services'] = Service.objects.all().order_by('id')
        context['service_fields'] = Field.objects.all().order_by('id')
        context['research_areas'] = ResearchArea.objects.all().order_by('id')
        context['tutorials'] = Tutorial.objects.all().order_by('id')
        context['news'] = News.objects.all().order_by('-id')[int(self.kwargs['pk']) - 1]
        return context


class ShowNewsList(ListView):
    model = News
    template_name = 'news/show_news_list.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['product_categories'] = Category.objects.filter(is_active=True).order_by('id')
        context['services'] = Service.objects.all().order_by('id')
        context['service_fields'] = Field.objects.all().order_by('id')
        context['research_areas'] = ResearchArea.objects.all().order_by('id')
        context['tutorials'] = Tutorial.objects.all().order_by('id')
        return context


class ShowNewsListAdmin(ListView, FormView):
    model = News
    template_name = 'news/show_news_list_admin.html'
    success_url = reverse_lazy('news:show_news_list_admin')
    form_class = NewsListAdminForm

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['product_categories'] = Category.objects.filter(is_active=True).order_by('id')
        context['services'] = Service.objects.all().order_by('id')
        context['service_fields'] = Field.objects.all().order_by('id')
        context['research_areas'] = ResearchArea.objects.all().order_by('id')
        context['tutorials'] = Tutorial.objects.all().order_by('id')
        return context

    def form_valid(self, form):
        News.objects.filter(id=form.cleaned_data['news_id']).delete()
        return super().form_valid(form)
