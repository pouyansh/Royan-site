from django.urls import path

from apps.temporary.views import *

urlpatterns = [
    path('register_template/', register, name='register'),
    path('submit_primer_1/', submit_primer_1, name='submit_primer_1'),
    path('submit_primer_4/', submit_primer_4, name='submit_primer_4'),
    path('service_description/', service_description, name='service_description'),
    path('index/', index, name='index'),
    path('user_profile/', user_profile, name='user_profile'),
    path('admin_profile/', admin_profile, name='admin_profile'),
    path('order_details/', order_details, name='order_details'),
    path('change_order/', change_order, name='change_order'),
]
