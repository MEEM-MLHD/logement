# -*- coding: utf-8 -*-
# Generated by Django 1.10 on 2017-02-17 11:14
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('appli', '0013_auto_20170216_1429'),
    ]

    operations = [
        migrations.AddField(
            model_name='city',
            name='name',
            field=models.CharField(default='', max_length=120, verbose_name='Nom de la commune'),
        ),
    ]
