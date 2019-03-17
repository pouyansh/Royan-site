from django.conf.urls import url
from django.urls import path

from apps.landing.views import *

urlpatterns = [
    path('/', index, name='index'),
]
