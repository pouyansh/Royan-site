from django.urls import path

from apps.temporary.views import *

urlpatterns = [
    path('register/', register, name='register'),
    path('submit_primer_1/', submit_primer_1, name='submit_primer_1'),
    path('submit_primer_2/', submit_primer_2, name='submit_primer_2'),
]
