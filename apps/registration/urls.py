from django.conf.urls import url
from django.urls import path

from apps.registration.views import *

urlpatterns = [
    path('login/', Login.as_view(), name='login'),
    path('login_success/', LoginSuccess.as_view(), name='login_success'),
    path('logout/', Logout.as_view(), name='logout'),
    path('register_person/', RegisterPerson.as_view(), name='register_person'),
    path('register_organization/', RegisterOrganization.as_view(), name='register_organization'),
    path('register_success/', RegisteredSuccessfully.as_view(), name='registered'),
    url(r'verify_email/(?P<keyword>\w+)/', VerifyEmail.as_view(), name='verify_email'),
    path('verified/', VerifiedSuccessfully.as_view(), name='verified'),
    path('verify_error/', VerifiedNotSuccessfully.as_view(), name='not_verified'),
]
