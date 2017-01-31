# -*- coding: utf-8 -*-
from collections import Counter
from datetime import datetime
import json
import requests
import subprocess
import xml.etree.ElementTree

from django.http import JsonResponse
from django.shortcuts import render, redirect
from django.contrib.sites.models import Site
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required

from djgeojson.serializers import Serializer as GeoJSONSerializer

#from .forms import ContributionForm
from .models import Actor, Contact, Experience, Participation, Tag, City
from .filters import ExperienceFilter

def consulter(request):
    experiences = Experience.objects.all()
    queryset = Experience.objects.all()
    f = ExperienceFilter(request.GET, queryset=queryset)
    
    search = False
    if len(request.GET) > 0:

        search = True

    geojson = GeoJSONSerializer().serialize(f.qs,
        geometry_field=('centroide'),
        properties=('nom', 'libelle_court', 'statut', 'statut_'))
    return render(request, 'consulter.html', {
        'filter': f,
        'experiences': experiences,
        'geojson': geojson,
        'search': search,
    })  