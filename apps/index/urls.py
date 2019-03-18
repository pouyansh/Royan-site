from django.conf.urls import url
from django.contrib.admin.views.decorators import staff_member_required
from django.urls import path

from apps.index.views import *

urlpatterns = [
    path('', Index.as_view(), name='index'),
    path('add_news/', staff_member_required(AddNews.as_view()), name='add_news')
]