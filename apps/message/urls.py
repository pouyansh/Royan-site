from django.conf.urls import url
from django.urls import path

from apps.message.views import *

urlpatterns = [
    url('create_message/', CustomerCreateMessage.as_view(), name='customer_create_message'),
]
