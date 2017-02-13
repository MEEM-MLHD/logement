# -*- coding: utf-8 -*-
import django_filters
from django import forms

from appli.models import Experience


class ExperienceFilter(django_filters.FilterSet):
    #experiences = django_filters.filters.ModelMultipleChoiceFilter(queryset=Experience.objects.all(), widget=forms.CheckboxSelectMultiple, label="Expériences")
 
    class Meta:
        model = Experience
        fields = {
			'name': ['contains'],
			'description_short': ['contains']
        }
        together = ['name', 'description_short']
