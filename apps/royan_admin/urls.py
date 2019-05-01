from django.conf.urls import url
from django.contrib.admin.views.decorators import staff_member_required
from django.urls import path

from apps.royan_admin.views import *

urlpatterns = [
    path('admin_panel/', staff_member_required(AdminPanel.as_view()), name='admin_panel'),
    url('customer_details/(?P<pk>[0-9]+)/', staff_member_required((CustomerDetails.as_view())), name='customer_profile')
]
