from django.conf.urls import url
from django.contrib.admin.views.decorators import staff_member_required
from django.urls import path

from apps.product.views import *

urlpatterns = [
    path('add_category/', staff_member_required(CreateCategory.as_view()), name='add_category'),
]
