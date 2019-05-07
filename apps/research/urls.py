from django.conf.urls import url
from django.contrib.admin.views.decorators import staff_member_required
from django.urls import path

from apps.research.views import *

urlpatterns = [
    path('research/create/', staff_member_required(AddResearchArea.as_view()), name='add_research_area'),
    url('research/edit/(?P<pk>[0-9]+)/$', staff_member_required(UpdateResearchArea.as_view()),
        name='update_research_area'),
    url('research/details/(?P<pk>[0-9]+)/$', ShowResearchAreaDetail.as_view(), name='show_research_area'),
    path('research/list/admin/', staff_member_required(ShowResearchAreaListAdmin.as_view()),
         name='show_research_area_list_admin'),
    path('research/choose/', staff_member_required(ChooseResearchArea.as_view()), name='choose_research_area'),
    url('paper/create/(?P<pk>[0-9]+)/$', staff_member_required(CreatePaper.as_view()), name='add_paper'),
    url('paper/edit/(?P<pk>[0-9]+)/$', staff_member_required(UpdatePaper.as_view()), name='update_paper'),
    url('paper/details/(?P<pk>[0-9]+)/$', ShowPaperDetail.as_view(), name='show_paper'),
    path('paper/list/admin/', staff_member_required(ShowPaperListAdmin.as_view()), name='show_paper_list_admin'),
]
