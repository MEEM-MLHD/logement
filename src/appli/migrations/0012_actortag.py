# -*- coding: utf-8 -*-
# Generated by Django 1.10 on 2017-02-16 11:19
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('appli', '0011_auto_20170216_1113'),
    ]

    operations = [
        migrations.CreateModel(
            name='ActorTag',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('tag', models.CharField(max_length=120)),
                ('actor', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='appli.Actor')),
            ],
        ),
    ]
