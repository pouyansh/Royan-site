from django.conf.urls import url
from django.urls import path

from apps.order.views import *

urlpatterns = [
    url('start_order_service/(?P<pk>[0-9]+)/', StartOrderService.as_view(), name='start_order'),
    url('order_service/(?P<pk>[0-9]+)/', SubmitOrderService.as_view(), name='order_service')
]
