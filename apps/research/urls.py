from django.conf.urls import url
from django.urls import path

from apps.research.views import *

urlpatterns = [
    path('create_research_area/', AddResearchArea.as_view(), name='add_research_area'),
]
