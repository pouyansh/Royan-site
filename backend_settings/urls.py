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

admin.site.site_header = "رویان توکاژن"
urlpatterns = [

                  url(r'^media/(?P<path>.*)$', django.views.static.serve,
                      {'document_root': settings.MEDIA_ROOT, 'show_indexes': settings.DEBUG}),
                  path('admin/', admin.site.urls),
                  path('', include(('apps.temporary.urls', 'temporary'), 'temporary')),
                  path('', include(('apps.registration.urls', 'registration'), 'registration')),
                  path('', include(('apps.news.urls', 'news'), 'news')),
                  path('', include(('apps.index.urls', 'index'), 'index')),

              ] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
