# -*- coding: utf-8 -*-
from django.contrib import admin

from .models import *


class TagInline(admin.TabularInline):
	model = Tag
	extra = 1


class EngagementInline(admin.TabularInline):
	model = Engagement
	extra = 1


class ParticipationInline(admin.TabularInline):
	model = Participation
	extra = 1


class ContactInline(admin.TabularInline):
    model = Contact
    extra = 1


class CityAdmin(admin.ModelAdmin):
    list_display = ('id','insee', )
    list_editable = ('insee', )


class ActorAdmin(admin.ModelAdmin):
    list_display = ('id','name', 'description_short', )
    search_fields = ('name', 'description_short', )


class ContactAdmin(admin.ModelAdmin):
    list_display = ('id','last_name', 'first_name', )


class ExperienceAdmin(admin.ModelAdmin):
    list_display = ('id','name', 'description_short')
    inlines = (EngagementInline,)
    search_fields = ('name', 'description_short', )
    list_filter = ('status', )


admin.site.register(Actor, ActorAdmin)
admin.site.register(Contact, ContactAdmin)
admin.site.register(Experience, ExperienceAdmin)
admin.site.register(City, CityAdmin)
admin.site.register(Tag)
admin.site.register(Event)
