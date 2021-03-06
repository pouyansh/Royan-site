from django.conf.urls import url
from django.contrib.admin.views.decorators import staff_member_required
from django.urls import path

from apps.service.views import *

urlpatterns = [
    path('create_field/', staff_member_required(CreateField.as_view()), name='create_field'),
    path('create_field_level2/', staff_member_required(CreateField2.as_view()), name='create_field2'),
    path('field_list_admin/', staff_member_required(ShowFieldListAdmin.as_view()), name='show_field_list_admin'),
    path('field2_list_admin/', staff_member_required(ShowField2ListAdmin.as_view()), name='show_field2_list_admin'),
    url('update_field/(?P<pk>[0-9]+)/', staff_member_required(UpdateField.as_view()), name='update_field'),
    url('update_field2/(?P<pk>[0-9]+)/', staff_member_required(UpdateField2.as_view()), name='update_field2'),
    path('delete_field_unsuccessful/', staff_member_required(DeleteFieldUnsuccessful.as_view()),
         name='delete_field_unsuccessful'),
    path('delete_field_successful/', staff_member_required(DeleteFieldSuccessful.as_view()),
         name='delete_field_successful'),
    url('field_details/(?P<pk>[0-9]+)/', FieldDetails.as_view(), name='field_details'),
    url('field_level2_details/(?P<pk>[0-9]+)/', Field2Details.as_view(), name='field2_details'),
    path('create_service/', staff_member_required(CreateService.as_view()), name='create_service'),
    url('service_details/(?P<pk>[0-9]+)/', ServiceDetails.as_view(), name='service_details'),
    path('service_list_admin/', staff_member_required(ShowServiceListAdmin.as_view()), name='show_service_list_admin'),
    url('update_service/(?P<pk>[0-9]+)/', staff_member_required(UpdateService.as_view()), name='update_service'),
    path('delete_service_successful/', staff_member_required(DeleteServiceSuccessful.as_view()),
         name='delete_service_successful'),
    url('create_form/(?P<pk>[0-9]+)/', staff_member_required(CreateFormForService.as_view()), name='create_form'),
]
