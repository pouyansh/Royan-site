from django.urls import path

from apps.index.views import *

urlpatterns = [
    path('', Index.as_view(), name='index'),
]
