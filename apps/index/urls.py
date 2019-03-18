from django.conf.urls import url
from django.urls import path

from apps.index.views import *

urlpatterns = [
    path('', Index.as_view(), name='index'),
    path('add_news/', AddNews.as_view(), name='add_news')
]