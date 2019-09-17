from django.conf.urls import url
from django.contrib.admin.views.decorators import staff_member_required
from django.urls import path

from apps.royan_admin.views import *

urlpatterns = [
    path('admin_panel/', staff_member_required(AdminPanel.as_view()), name='admin_panel'),
    url('customer_details/(?P<pk>[0-9]+)/', staff_member_required((CustomerDetails.as_view())),
        name='customer_profile'),
    url('update_info/(?P<pk>[0-9]+)/', staff_member_required((ChangeSystemInformation.as_view())),
        name='update_info'),
    url('block_user/(?P<pk>[0-9]+)/', staff_member_required(BlockUser.as_view()), name='block'),
    url('unblock_user/(?P<pk>[0-9]+)/', staff_member_required(UnblockUser.as_view()), name='unblock'),
    path('blocked/', staff_member_required(BlockSuccessful.as_view()), name='blocked'),
    path('unblocked/', staff_member_required(UnlockSuccessful.as_view()), name='unblocked'),
]
