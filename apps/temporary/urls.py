from django.urls import path

from apps.temporary.views import *

urlpatterns = [
    path('register/', register, name='register'),
]
