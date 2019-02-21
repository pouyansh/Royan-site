from django.contrib import admin

# Register your models here.
from apps.registration.models import *

admin.site.register(Customer)
admin.site.unregister(User)
