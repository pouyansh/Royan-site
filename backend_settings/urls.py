from django.conf import settings
from django.conf.urls.static import static

"""asd URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.conf.urls import url
import django.views.static

admin.site.site_header = "Royan TuCAGene"
urlpatterns = [

                  url(r'^media/(?P<path>.*)$', django.views.static.serve,
                      {'document_root': settings.MEDIA_ROOT, 'show_indexes': settings.DEBUG}),
                  path('admin/', admin.site.urls),
                  path('', include(('apps.temporary.urls', 'temporary'), 'temporary')),
                  path('', include(('apps.registration.urls', 'registration'), 'registration')),
                  path('', include(('apps.news.urls', 'news'), 'news')),
                  path('', include(('apps.product.urls', 'product'), 'product')),
                  path('', include(('apps.royan_admin.urls', 'royan_admin'), 'royan_admin')),
                  path('', include(('apps.service.urls', 'service'), 'service')),
                  path('', include(('apps.research.urls', 'research'), 'research')),
                  path('', include(('apps.tutorial.urls', 'tutorial'), 'tutorial')),
                  path('', include(('apps.order_service.urls', 'order_service'), 'order_service')),
                  path('', include(('apps.order_product.urls', 'order_product'), 'order_product')),
                  path('', include(('apps.dashboard.urls', 'dashboard'), 'dashboard')),
                  path('', include(('apps.message.urls', 'message'), 'message')),
                  path('', include(('apps.index.urls', 'index'), 'index')),

              ] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
