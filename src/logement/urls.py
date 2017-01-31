# -*- coding: utf-8 -*-
from django.conf.urls import url, include
from django.contrib import admin
from django.contrib.auth import views as auth_views

from appli.views import consulter


urlpatterns = [

    url(r'^admin/', admin.site.urls),
    # On import les vues de Django, avec un nom spécifique
    url(r'^consulter[//]*', consulter, name="consulter"),
    
]

admin.site.site_header = "logement"
