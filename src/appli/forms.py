# -*- coding: utf-8 -*-
from dal import autocomplete
from django.contrib.gis import forms


from .models import ExperienceTag


class ExperienceTagForm(forms.ModelForm):

    class Meta:
        model = ExperienceTag
        fields = ['tag',]
        widgets = {
            'tag': autocomplete.ModelSelect2Multiple(url='experiencetag-autocomplete', )
        }
