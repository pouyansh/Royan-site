from django.conf.urls import url
from django.contrib.admin.views.decorators import staff_member_required

from apps.order_product.views import *

urlpatterns = [
    url(r'order/product/start/(?P<pk>\w+)/', StartOrderProduct.as_view(), name='start_order'),
]
