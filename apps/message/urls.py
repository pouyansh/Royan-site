from django.conf.urls import url
from django.contrib.admin.views.decorators import staff_member_required
from django.urls import path

from apps.message.views import *

urlpatterns = [
    path('create_message/', CustomerCreateMessage.as_view(), name='customer_create_message'),
    url(r'create_message/admin/(?P<pk>[0-9]+)/', staff_member_required(AdminCreateMessage.as_view()),
        name="admin_create_message"),
]
