from django.conf.urls import url
from django.contrib.admin.views.decorators import staff_member_required
from django.urls import path

from apps.news.views import *

urlpatterns = [
    path('add_news/', staff_member_required(AddNews.as_view()), name='add_news')
]