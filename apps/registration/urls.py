from django.conf.urls import url
from django.urls import path

from apps.registration.views import *

urlpatterns = [
	path('register/', Register.as_view(), name='register'),
]
