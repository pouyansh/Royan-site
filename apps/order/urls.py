from django.conf.urls import url
from django.urls import path

from apps.order.views import *

urlpatterns = [
    path('order_service/', SubmitOrderService.as_view(), name='order_service')
]
