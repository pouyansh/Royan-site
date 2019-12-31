from django.conf.urls import url
from django.contrib.admin.views.decorators import staff_member_required

from apps.order_service.views import *

urlpatterns = [
    url(r'order/service/start/(?P<pk>.+)/', StartOrderService.as_view(), name='start_order'),
    url(r'order/service/order/(?P<pk>.+)/', SubmitOrderService.as_view(), name='order_service'),
    url(r'order/service/check_data/(?P<pk>.+)/', CheckData.as_view(), name='check_data'),
    url(r'order/service/get_code/(?P<pk>.+)/', GetCode.as_view(), name='get_code'),
    url(r'order/service/details/(?P<pk>.+)/', OrderDetails.as_view(), name='order_details'),
    url(r'order/service/received/(?P<pk>.+)/', CheckReceived.as_view(), name='order_received'),
    url(r'order/service/payed/(?P<pk>.+)/', staff_member_required(CheckPayed.as_view()), name='order_payed'),
    url(r'order/service/set_invoice/(?P<pk>.+)/', staff_member_required(SetInvoice.as_view()), name='set_invoice'),
    url(r'order/service/set_receiving_date/(?P<pk>.+)/', staff_member_required(SetReceivingDate.as_view()),
        name='set_receiving_date'),
    url(r'order/service/invoice/(?P<pk>.+)/', staff_member_required(CheckInvoice.as_view()), name='order_invoice'),
    url(r'order/service/error/columns/', FileErrorColumns.as_view(), name='file_error_columns'),
    url(r'order/service/error/number/', FileErrorNumber.as_view(), name='file_error_number'),
    url(r'order/service/error/oligo/', FileErrorOligo.as_view(), name='file_error_oligo'),
    url(r'order/service/error/incomplete/', FileErrorIncomplete.as_view(), name='file_error_incomplete')
]
