from django.conf.urls import url
from django.contrib.admin.views.decorators import staff_member_required
from django.urls import path

from apps.news.views import *

urlpatterns = [
    path('add_news/', staff_member_required(AddNews.as_view()), name='add_news'),
    path('news_list/', ShowNewsList.as_view(), name='show_news_list'),
    url('update_news/(?P<pk>[0-9]+)/$', UpdateNews.as_view(), name='update_news'),
    url('news/(?P<pk>[0-9]+)/$', ShowNewsDetail.as_view(), name='show_news'),
]
