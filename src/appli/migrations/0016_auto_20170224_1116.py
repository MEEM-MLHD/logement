# -*- coding: utf-8 -*-
# Generated by Django 1.10 on 2017-02-24 11:16
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('appli', '0015_auto_20170217_1115'),
    ]

    operations = [
        migrations.CreateModel(
            name='ActorTagOrder',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('order', models.PositiveIntegerField(verbose_name='n\xb0 ordre')),
                ('actor', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='appli.Actor')),
            ],
        ),
        migrations.CreateModel(
            name='ExperienceTagOrder',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('order', models.PositiveIntegerField(verbose_name='n\xb0 ordre')),
                ('experience', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='appli.Experience')),
            ],
        ),
        migrations.RemoveField(
            model_name='actortag',
            name='actor',
        ),
        migrations.RemoveField(
            model_name='experiencetag',
            name='experience',
        ),
        migrations.AddField(
            model_name='experiencetagorder',
            name='experience_tag',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='appli.ExperienceTag', verbose_name='Mot cl\xe9'),
        ),
        migrations.AddField(
            model_name='actortagorder',
            name='actor_tag',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='appli.ActorTag', verbose_name='Mot cl\xe9'),
        ),
        migrations.AddField(
            model_name='actor',
            name='tags',
            field=models.ManyToManyField(through='appli.ActorTagOrder', to='appli.ActorTag'),
        ),
        migrations.AddField(
            model_name='experience',
            name='tags',
            field=models.ManyToManyField(through='appli.ExperienceTagOrder', to='appli.ExperienceTag'),
        ),
    ]
