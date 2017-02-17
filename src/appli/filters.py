# -*- coding: utf-8 -*-
import django_filters

from .models import Experience


class ExperienceFilter(django_filters.FilterSet):

    class Meta:
        model = Experience

        fields = {
			'title': ['contains'],
			'description_short': ['contains'],
        }
        together = ['title', 'description_short']
