from django.conf.urls import url
from django.urls import path

from apps.index.views import *

urlpatterns = [
    path('', index, name='index'),
]