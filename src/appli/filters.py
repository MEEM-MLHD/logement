# -*- coding: utf-8 -*-
import django_filters

from .models import Experience


class ExperienceFilter(django_filters.FilterSet):

    class Meta:
        model = Experience
        fields = ['name', 'status', 'tags', ]
