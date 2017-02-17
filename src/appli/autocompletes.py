from dal import autocomplete

from .models import ExperienceTag


class ExperienceTagAutocomplete(autocomplete.Select2QuerySetView):
    def get_queryset(self):
        qs = ExperienceTag.objects.all().order_by('tag')
        if self.q:
            qs = qs.filter(tag__istartswith=self.q)
        return qs
