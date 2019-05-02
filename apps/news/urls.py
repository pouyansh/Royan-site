from django.conf.urls import url
from django.contrib.admin.views.decorators import staff_member_required
from django.urls import path

from apps.news.views import *

urlpatterns = [
    path('news/create/', staff_member_required(AddNews.as_view()), name='add_news'),
    path('news/all/', ShowNewsList.as_view(), name='show_news_list'),
    path('news/all/admin/', staff_member_required(ShowNewsListAdmin.as_view()), name='show_news_list_admin'),
    url(r'news/edit/(?P<pk>\w+)/$', staff_member_required(UpdateNews.as_view()), name='update_news'),
    url(r'news/details/(?P<pk>\w+)/$', ShowNewsDetail.as_view(), name='show_news'),
]
