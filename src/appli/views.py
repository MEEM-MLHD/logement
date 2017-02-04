# -*- coding: utf-8 -*-
from django.shortcuts import render

from djgeojson.serializers import Serializer as GeoJSONSerializer

from .models import Experience
from .filters import ExperienceFilter


def consulter(request):
    experiences = Experience.objects.all()
    queryset = Experience.objects.all()
    f = ExperienceFilter(request.GET, queryset=queryset)
    search = False
    if len(request.GET) > 0:
        search = True
    geojson = GeoJSONSerializer().serialize(f.qs,
        geometry_field=('centroid'),
        properties=('name', 'description_short', 'status', 'statusfr'))
    return render(request, 'consulter.html', {
        'filter': f,
        'experiences': experiences,
        'geojson': geojson,
        'search': search,
    })
