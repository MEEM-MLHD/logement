# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import requests
import json

from collections import defaultdict, Counter

from django.db import models
from django.db.models import Count
from django.contrib.gis.db import models as gis_models
from django.contrib.gis.geos import GEOSGeometry, GeometryCollection
from django.utils.text import slugify


class Actor(models.Model):
    name = models.CharField(max_length=120)
    address = models.CharField(max_length=240, blank=True)
    url = models.URLField(max_length=240, blank=True)
    city = models.ForeignKey('City', blank=True)
    description_short = models.CharField(max_length=120)
    description_long = models.TextField(blank=True)
    logo = models.ImageField(upload_to="actor/logo", blank=True, null=True)
    featured_image = models.ImageField(upload_to="actor/featured_image", blank=True)
    tags = models.ManyToManyField('Tag')

    class Meta:
        verbose_name = u"Acteur"

    def __unicode__(self):
        return self.name


class Contact(models.Model):
    first_name = models.CharField(max_length=120)
    last_name = models.CharField(max_length=120)
    title = models.CharField(max_length=120)
    email = models.EmailField(max_length=254, blank=True)
    phone = models.CharField(max_length=15, blank=True)
    description_short = models.CharField(max_length=120)
    description_long = models.TextField(blank=True, null=True)
    avatar = models.ImageField(upload_to="contact", blank=True, null=True)
    featured_image = models.ImageField(upload_to="contact/featured_image", blank=True)
    tags = models.ManyToManyField('Tag')
    actor = models.ForeignKey('Actor')
    
    def __unicode__(self):
        return "%s %s" % (self.first_name, self.last_name)


class Experience(models.Model):
    STATUS_CHOICES = (
        ('green', u'réalisé'),
        ('yellow', u'en cours'),
        ('teal', u'en projet'),
    )
    name = models.CharField(max_length=120)
    address = models.CharField(max_length=240)
    city = models.ForeignKey('City', blank=True, null=True)
    description_short = models.TextField(max_length=240)
    description_long = models.TextField(blank=True, null=True)
    status =  models.CharField(max_length=10, choices=STATUS_CHOICES, default='en projet')
    logo = models.ImageField(upload_to="experience", blank=True, null=True)
    featured_image = models.ImageField(upload_to="experience", blank=True, null=True)
    url = models.URLField(max_length=240)
    contacts =  models.ManyToManyField('Contact', through='Engagement')
    participants = models.ManyToManyField('Actor', through='Participation')
    tags = models.ManyToManyField('Tag')
    featured = models.BooleanField(default=False)
    create_date = models.DateTimeField(auto_now_add=True, blank=True, null=True)
    update_date = models.DateTimeField(auto_now=True, blank=True, null=True)

    class Meta:
        verbose_name = u"Expérience"

    def __unicode__(self):
        return self.nom

    @property
    def geometry(self):
        return self.city.geometry

    @property
    def centroide(self):
        return self.city.geometry.centroid

    @property
    def statusfr(self):
        return self.get_status_display()


class Event(models.Model):
    title = models.CharField(max_length=255)
    title_short = models.CharField(max_length=255)
    featured_image = models.ImageField(upload_to="events/featured_image")
    description = models.TextField()
    publication_date = models.DateField()
    deadline_date = models.DateField()

    featured = models.BooleanField()
    create_date = models.DateTimeField(auto_now_add=True)
    update_date = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = u"Evénement"

    def __unicode__(self):
        return self.title



class Engagement(models.Model):
    experience = models.ForeignKey(Experience)
    contact = models.ForeignKey(Contact)
    rank = models.PositiveIntegerField()


class Participation(models.Model):
    experience = models.ForeignKey(Experience)
    acteur = models.ForeignKey(Actor)
    rank = models.PositiveIntegerField()


class City(gis_models.Model):
    insee = models.CharField(max_length=5)
    geometry = gis_models.GeometryCollectionField(blank=True, null=True)

    def save(self, *args, **kwargs):
        if self.geometry :
            pass
        else :
            r = requests.get('https://geo.api.gouv.fr/communes?fields=contour&code=%s' % (self.insee))
            try:
                coord = r.json()[0]['contour']
            except:
                pass
            try:
                mpoly = GEOSGeometry(json.dumps(coord))
                self.geometry = GeometryCollection(mpoly)
            except:
                pass   
        super(Commune, self).save(*args, **kwargs)


    def centroide(self):
        return self.geometry.centroid

    def __unicode__(self):
        return self.insee


class Tag(models.Model):
    tag = models.CharField(max_length=120)

    def __unicode__(self):
        return self.tag

class ActorImage(models.Model):
    actor = models.ForeignKey(Experience)
    file = models.ImageField(upload_to='images')
    title = models.CharField(max_length=255, blank=True)

    class Meta:
        verbose_name = u"Image"

    def __unicode__(self):
        return self.title

class ExperienceImage(models.Model):
    file = models.ImageField(upload_to='images')
    title = models.CharField(max_length=255, blank=True)

    class Meta:
        verbose_name = u"Image"

    def __unicode__(self):
        return self.title
