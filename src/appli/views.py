# -*- coding: utf-8 -*-
from django.shortcuts import render

from djgeojson.serializers import Serializer as GeoJSONSerializer

from .filters import ExperienceFilter
from .models import Experience


def consulter(request):
    experiences = Experience.objects.all()
    f = ExperienceFilter(request.GET, queryset=Experience.objects.all())
    search = False
    if len(request.GET) > 0:
        search = True
    geojson = GeoJSONSerializer().serialize(f.qs,
                                            geometry_field=('centroid'),
                                            properties=('title', 'description_short',
                                                        'status', 'statusfr'))
    return render(request, 'consulter.html', {
        'filter': f,
        'experiences': experiences,
        'geojson': geojson,
        'search': search,
    })

def consulter_experience(request, id):
    experiences = Experience.objects.get(id=id)
    geojson = GeoJSONSerializer().serialize(experiences,
        geometry_field=('centroid'),
        properties=('title', 'description_short', 'status', 'statusfr'))
    return render(request, 'consulter_experience.html', {
        'experiences': experiences,
        'geojson': geojson,
    })

def experience_(request, id):
    experiences = Experience.objects.get(id=id)
    geojson = GeoJSONSerializer().serialize(experiences,
        geometry_field=('centroid'),
        properties=('title', 'description_short', 'status', 'statusfr'))
    return render(request, 'consulter_.html', {
        'experiences': experiences,
        'geojson': geojson,
    })
