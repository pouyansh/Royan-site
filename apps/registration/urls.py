from django.conf.urls import url
from django.urls import path

from apps.registration.views import *

urlpatterns = [
    path('login/', Login.as_view(), name='login'),
    path('login_success/', LoginSuccess.as_view(), name='login_success'),
    path('logout/', Logout.as_view(), name='logout'),
    path('register/', RegisterUser.as_view(), name='register'),
    path('register_person/', RegisterPerson.as_view(), name='register_person'),
]
