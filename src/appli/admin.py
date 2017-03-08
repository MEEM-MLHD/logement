# -*- coding: utf-8 -*-
from django.contrib import admin
from leaflet.admin import LeafletGeoAdmin
from markdownx.admin import MarkdownxModelAdmin

from .models import *



class ActorTagOrderInline(admin.TabularInline):
    model = ActorTagOrder
    extra = 1


class ExperienceTagOrderInline(admin.TabularInline):
    model = ExperienceTagOrder
    extra = 1


class ExperienceImageInline(admin.TabularInline):
    model = ExperienceImage
    extra = 1


class ActorImageInline(admin.TabularInline):
    model = ActorImage
    extra = 1


class EngagementInline(admin.TabularInline):
    model = Engagement
    extra = 1


class ParticipationInline(admin.TabularInline):
    model = Participation
    extra = 1


class ContactInline(admin.TabularInline):
    model = Contact


class CityAdmin(admin.ModelAdmin):
    list_display = ('id', 'insee', 'name')

    class Media:
        css = {
            #"all": ("https://cdnjs.cloudflare.com/ajax/libs/select2/4.0.3/css/select2.min.css",)
            "all": ("select2.css",)
        }
        #js = ("https://code.jquery.com/jquery-3.1.1.min.js", 'https://cdnjs.cloudflare.com/ajax/libs/select2/4.0.3/js/select2.full.min.js', "city.js",)
        js = ("jquery-3.1.1.min.js", 'select2.full.min.js', "city.js",)


class ActorAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'description_short', )
    inlines = (ParticipationInline, ActorImageInline, ActorTagOrderInline,)
    search_fields = ('name', 'description_short', )


class ContactAdmin(admin.ModelAdmin):
    list_display = ('id', 'last_name', 'first_name', )


class ExperienceAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'description_short', )
    inlines = (EngagementInline, ParticipationInline, ExperienceImageInline, ExperienceTagOrderInline, )
    search_fields = ('title', 'description_short', )
    list_filter = ('status', )



admin.site.register(Actor, ActorAdmin)
admin.site.register(City, CityAdmin)
admin.site.register(Contact, ContactAdmin)
admin.site.register(Event)
admin.site.register(Experience, ExperienceAdmin)
admin.site.register(ExperienceTag)
admin.site.register(ActorTag)
