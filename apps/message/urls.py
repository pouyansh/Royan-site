from django.conf.urls import url
from django.contrib.admin.views.decorators import staff_member_required
from django.urls import path

from apps.message.views import *

urlpatterns = [
    path('message/send/', CustomerCreateMessage.as_view(), name='customer_create_message'),
    url(r'message/send/admin/(?P<username>\w+)/', staff_member_required(AdminCreateMessage.as_view()),
        name="admin_create_message"),
    url(r'message/details/(?P<pk>\w+)/', MessageDetails.as_view(), name="message_details")
]
