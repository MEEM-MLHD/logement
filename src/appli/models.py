# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import json
import requests
from markdownx.models import MarkdownxField

from django.contrib.gis.db import models as gis_models
from django.contrib.gis.geos import GEOSGeometry, GeometryCollection
from django.db import models



 

class Actor(models.Model):
    """Actor model
    Define an actor of an Experience, someone really involved in the housing experience.
    """
    name = models.CharField(u'nom', max_length=120)
    address = models.CharField(u'adresse', max_length=240, blank=True)
    url = models.URLField(max_length=240, blank=True)
    city = models.ForeignKey('City', verbose_name=u'ville', blank=True)
    description_short = models.CharField(u'description courte', max_length=120)
    description_long = MarkdownxField(u'description longue', default="#### Titre", null=True)
    logo = models.ImageField(upload_to="actor/logo", blank=True, null=True)
    featured_image = models.ImageField(u'image de couverture', upload_to="actor/featured_image", blank=True)
    featured = models.BooleanField(u'à la une', default=False)
    share_contact_ref = models.BooleanField(u'autorise la transmission des coordonnées des contacts', default=False)
    tags = models.ManyToManyField('ActorTag', through='ActorTagOrder')

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
    detail = models.TextField(u"complément", blank=True, null=True)
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
    description_long = MarkdownxField(u'description longue', default="#### Titre", null=True)
    status =  models.CharField(max_length=10, choices=STATUS_CHOICES, default='en projet')
    featured_image = models.ImageField(u'image de couverture', upload_to="experience", blank=True, null=True)
    featured_image_txt = models.TextField(u'légende, crédit photo...', max_length=240, blank=True, default="")
    url = models.URLField(max_length=240, blank=True)
    contacts =  models.ManyToManyField('Contact', through='Engagement')
    participants = models.ManyToManyField('Actor', through='Participation')
    tags = models.ManyToManyField('ExperienceTag', through='ExperienceTagOrder')
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
    description_long =MarkdownxField(u'decription longue', null=True)
    publication_date = models.DateField(u'date de publication')
    deadline_date = models.DateField(u'date de fin de publication')
    url = models.URLField(max_length=240, blank=True)
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
        if self.geometry:
            pass
        else:
            if self.insee in ["75101", "75102", "75103", "75104", "75105", "75106", "75107", "75108", "75109", "75110", "75111", "75112", "75113","75114", "75115", "75116", "75117", "75118", "75119", "75120"]:
                code_INSEE = "75056"
            elif self.insee in ["69381", "69382", "69383", "69384", "69385", "69386", "69387", "69388", "69389"]:
                code_INSEE = "69123"
            elif self.insee in ["13201", "13202", "13203", "13204", "13205", "13206", "13207", "13208", "13209", "13210", "13211", "13212", "13213","13214", "13215", "13216"]:
                code_INSEE = "13055" 
            else:
                code_INSEE = self.insee            
            r = requests.get('https://geo.api.gouv.fr/communes?fields=nom,contour&code=%s' % (code_INSEE))
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
    tag = models.CharField(max_length=120)

    def __unicode__(self):
        return self.tag

    class Meta:
        verbose_name = u"Mots-clé Expérience"


class ExperienceTagOrder(models.Model):
    experience_tag = models.ForeignKey(ExperienceTag, verbose_name=u'Mot clé',)
    experience = models.ForeignKey(Experience)
    order = models.PositiveIntegerField(u'n° ordre')

    class Meta:
        verbose_name = u"Relation Experience - Mots-clé"


class ActorTag(models.Model):
    tag = models.CharField(max_length=120)

    def __unicode__(self):
        return self.tag

    class Meta:
        verbose_name = u"Mots-clé Acteur"


class ActorTagOrder(models.Model):
    actor_tag = models.ForeignKey(ActorTag, verbose_name=u'Mot clé')
    actor = models.ForeignKey(Actor)
    order = models.PositiveIntegerField(u'n° ordre')

    class Meta:
        verbose_name = u"Relation Acteur - Mots-clé"


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
