from django.conf.urls import url

from apps.order_service.views import *

urlpatterns = [
    url('order/service/start/(?P<pk>[0-9]+)/', StartOrderService.as_view(), name='start_order'),
    url('order/service/(?P<pk>[0-9]+)/', SubmitOrderService.as_view(), name='order_service'),
    url('order/service/check_data/(?P<pk>[0-9]+)/', CheckData.as_view(), name='check_data'),
    url('order/service/get_code/(?P<pk>[0-9]+)/', GetCode.as_view(), name='get_code'),
    url('order/service/details/(?P<pk>[0-9]+)/', OrderDetails.as_view(), name='order_details')
]
