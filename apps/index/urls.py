from django.urls import path

from apps.index.views import *

urlpatterns = [
    path('about/', About.as_view(), name='about'),
    path('contact/', Contact.as_view(), name='contact'),
    path('', Index.as_view(), name='index'),
]
