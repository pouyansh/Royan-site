from django.conf.urls import url
from django.urls import path

from apps.order_service.views import *

urlpatterns = [
    url('start_order_service/(?P<pk>[0-9]+)/', StartOrderService.as_view(), name='start_order'),
    url('order_service/(?P<pk>[0-9]+)/', SubmitOrderService.as_view(), name='order_service'),
    url('check_data/(?P<pk>[0-9]+)/', CheckData.as_view(), name='check_data'),
    url('get_code/(?P<pk>[0-9]+)/', GetCode.as_view(), name='get_code')
]
