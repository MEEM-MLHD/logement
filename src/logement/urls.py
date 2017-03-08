# -*- coding: utf-8 -*-
from django.conf.urls import url, include
from django.contrib import admin
from django.contrib.auth import views as auth_views

from appli.views import consulter, consulter_experience, experience_
from appli.autocompletes import ExperienceTagAutocomplete





urlpatterns = [

    url(r'^admin/', admin.site.urls),
    # On import les vues de Django, avec un nom spécifique
    url(r'^consulter[//]*', consulter, name="consulter"),
    url(r'^experience_/(?P<id>\d+)/$', experience_, name="experience_"),
    url(r'^tinymce/', include('tinymce.urls')),
    url(r'^experiencetag-autocomplete/$', ExperienceTagAutocomplete.as_view(), name='experiencetag-autocomplete'),

    
]

admin.site.site_header = "logement"
