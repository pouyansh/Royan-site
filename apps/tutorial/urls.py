from django.conf.urls import url
from django.contrib.admin.views.decorators import staff_member_required
from django.urls import path

from apps.tutorial.views import *

urlpatterns = [
    path('tutorial/create/', staff_member_required(AddTutorial.as_view()), name='add_tutorial'),
    url('tutorial/edit/(?P<pk>[0-9]+)/$', staff_member_required(UpdateTutorial.as_view()), name='update_tutorial'),
    url('tutorial/details/(?P<pk>[0-9]+)/$', ShowTutorialDetail.as_view(), name='show_tutorial'),
    path('tutorial/choose/', staff_member_required(ChooseTutorial.as_view()), name='choose_tutorial'),
    path('tutorial/list/admin/', staff_member_required(ShowTutorialListAdmin.as_view()),
         name='show_tutorial_list_admin'),
    url('link/create/(?P<pk>[0-9]+)/$', staff_member_required(CreateLink.as_view()), name='add_link'),
    url('link/edit/(?P<pk>[0-9]+)/$', staff_member_required(UpdateLink.as_view()), name='update_link'),
    url('tutorial/workshop/(?P<pk>[0-9]+)/$', ShowLink.as_view(), name='show_details'),
    path('tutorial/workshop/list/admin/', staff_member_required(ShowWorkshopListAdmin.as_view()),
         name='show_workshop_list_admin'),
]
