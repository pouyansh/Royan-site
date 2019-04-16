from django.conf.urls import url
from django.contrib.admin.views.decorators import staff_member_required
from django.urls import path

from apps.research.views import *

urlpatterns = [
    path('create_research_area/', staff_member_required(AddResearchArea.as_view()), name='add_research_area'),
    url('update_research_area/(?P<pk>[0-9]+)/$', staff_member_required(UpdateResearchArea.as_view()),
        name='update_research_area'),
    url('research_area/(?P<pk>[0-9]+)/$', ShowResearchAreaDetail.as_view(), name='show_research_area'),
    path('research_area_list_admin/', staff_member_required(ShowResearchAreaListAdmin.as_view()),
         name='show_research_area_list_admin'),
    path('choose_research_area/', staff_member_required(ChooseResearchArea.as_view()), name='choose_research_area'),
    url('create_paper/(?P<pk>[0-9]+)/$', staff_member_required(CreatePaper.as_view()), name='add_paper'),
    url('update_paper/(?P<pk>[0-9]+)/$', staff_member_required(UpdatePaper.as_view()), name='update_paper'),
    url('paper/(?P<pk>[0-9]+)/$', ShowPaperDetail.as_view(), name='show_paper'),
    path('paper_list_admin/', staff_member_required(ShowPaperListAdmin.as_view()), name='show_paper_list_admin'),
]
