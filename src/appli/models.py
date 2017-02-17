# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import json
import requests

from django.contrib.gis.db import models as gis_models
from django.contrib.gis.geos import GEOSGeometry, GeometryCollection
from django.db import models
from tinymce.models import HTMLField




class Actor(models.Model):
    name = models.CharField(u'nom', max_length=120)
    address = models.CharField(u'adresse', max_length=240, blank=True)
    url = models.URLField(max_length=240, blank=True)
    city = models.ForeignKey('City', verbose_name=u'ville', blank=True)
    description_short = models.CharField(u'description courte', max_length=120)
    description_long = HTMLField(u'description longue', default="<h3>Titre</h3></hgroup><p>Paragraph</p><h3>Titre</h3></hgroup><p>Paragraph</p>", null=True)
    logo = models.ImageField(upload_to="actor/logo", blank=True, null=True)
    featured_image = models.ImageField(u'image de couverture', upload_to="actor/featured_image", blank=True)
    featured = models.BooleanField(u'à la une', default=False)
    share_contact_ref = models.BooleanField(u'autorise la transmission des coordonnées des contacts', default=False)

    def __unicode__(self):
        return self.name

    class Meta:
        verbose_name = u"Acteur"


class Contact(models.Model):
    first_name = models.CharField(u'prénom', max_length=120)
    last_name = models.CharField(u'nom', max_length=120)
    description_short = models.CharField(u'description courte', max_length=120, default="")
    email = models.EmailField(u'courriel', max_length=254, blank=True)
    phone = models.CharField(u'téléphone', max_length=15, blank=True)
    detail = models.TextField(blank=True, null=True)
    photo = models.ImageField(upload_to="contact", blank=True, null=True)
    actor = models.ForeignKey('Actor', verbose_name=u'acteur')

    def __unicode__(self):
        return "%s %s" % (self.first_name, self.last_name)


class Experience(models.Model):
    STATUS_CHOICES = (
        ('green', u'réalisé'),
        ('yellow', u'en cours'),
        ('teal', u'en projet'),
    )
    title = models.CharField(u'titre', max_length=120)
    subtitle = models.CharField(u'sous-titre', max_length=240)
    city = models.ForeignKey('City',verbose_name=u'ville', blank=True, null=True)
    description_short = models.TextField(u'description courte', max_length=240)
    description_long = HTMLField(u'description longue', default="<h3>Titre</h3></hgroup><p>Paragraph</p><h3>Titre</h3></hgroup><p>Paragraph</p>", null=True)
    status =  models.CharField(max_length=10, choices=STATUS_CHOICES, default='en projet')
    featured_image = models.ImageField(u'image de couverture', upload_to="experience", blank=True, null=True)
    featured_image_txt = models.TextField(u'légende, crédit photo...', max_length=240, blank=True, default="")
    url = models.URLField(max_length=240, blank=True)
    contacts =  models.ManyToManyField('Contact', through='Engagement')
    participants = models.ManyToManyField('Actor', through='Participation')
    featured = models.BooleanField(u'à la une', default=False)
    create_date = models.DateTimeField(u'date de création', auto_now_add=True, blank=True, null=True)
    update_date = models.DateTimeField(u'date de mise à jour', auto_now=True, blank=True, null=True)

    def __unicode__(self):
        return self.title

    @property
    def geometry(self):
        return self.city.geometry

    @property
    def centroid(self):
        return self.city.geometry.centroid

    @property
    def statusfr(self):
        return self.get_status_display()

    class Meta:
        verbose_name = u"Expérience"


class Event(models.Model):
    title = models.CharField(u'titre', max_length=120)
    subtitle = models.CharField(u'sous-titre', max_length=240, default="")
    featured_image = models.ImageField(u'image de couverture', upload_to="events/featured_image")
    description_short = models.TextField(u'description courte', max_length=240, default="")
    description_long =HTMLField(u'decription longue', null=True)
    publication_date = models.DateField(u'date de publication')
    deadline_date = models.DateField(u'date de fin de publication')
    url = models.URLField(max_length=240, blank=True)
    #featured = models.BooleanField(u'à la une')
    create_date = models.DateTimeField(u'date de création', auto_now_add=True)
    update_date = models.DateTimeField(u'date de mise à jour', auto_now=True)

    def __unicode__(self):
        return self.title

    class Meta:
        verbose_name = u"Evénement"


class Engagement(models.Model):
    experience = models.ForeignKey(Experience)
    contact = models.ForeignKey(Contact)
    rank = models.PositiveIntegerField(u'n° ordre')

    class Meta:
        verbose_name = u"Contact"

class Participation(models.Model):
    experience = models.ForeignKey(Experience)
    acteur = models.ForeignKey(Actor)
    rank = models.PositiveIntegerField(u'n° ordre')

    class Meta:
        verbose_name = u"Participant"


class City(gis_models.Model):
    insee = models.CharField(u'code INSEE de la commune', max_length=5)
    name = models.CharField(u'Nom de la commune', max_length=120, default="", blank=True)
    geometry = gis_models.GeometryCollectionField(blank=True, null=True)

    def save(self, *args, **kwargs):
        if self.geometry :
            pass
        else :
            r = requests.get('https://geo.api.gouv.fr/communes?fields=nom,contour&code=%s' % (self.insee))
            try:
                coord = r.json()[0]['contour']
                nom = r.json()[0]['nom']
            except:
                pass
            try:
                mpoly = GEOSGeometry(json.dumps(coord))
                self.geometry = GeometryCollection(mpoly)
                self.name = nom
            except:
                pass
        super(City, self).save(*args, **kwargs)


    def centroid(self):
        return self.geometry.centroid

    def __unicode__(self):
        return "%s (insee : %s)" % (self.name, self.insee)

    class Meta:
        verbose_name = u"Localisation"


class ExperienceTag(models.Model):
    experience = models.ForeignKey(Experience)
    tag = models.CharField(max_length=120)

    def __unicode__(self):
        return self.tag


class ActorTag(models.Model):
    actor = models.ForeignKey(Actor)
    tag = models.CharField(max_length=120)

    def __unicode__(self):
        return self.tag


class ActorImage(models.Model):
    actor = models.ForeignKey(Actor)
    file = models.ImageField(u'fichier', upload_to='images')
    title = models.CharField(u'titre, crédit...', max_length=255, blank=True)

    def __unicode__(self):
        return self.title

    class Meta:
        verbose_name = u"Image_Acteur"


class ExperienceImage(models.Model):
    file = models.ImageField(u'fichier', upload_to='images')
    title = models.CharField(u'titre, crédit...', max_length=255, blank=True)
    experience = models.ForeignKey(Experience, null=True)

    def __unicode__(self):
        return self.title

    def image_tag(self):
        return u'<img src="%s" />' % (self.file.url)
    image_tag.short_description = 'Image'
    image_tag.allow_tags = True

    class Meta:
        verbose_name = u"Image_Experience"
