# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.AutoField(primary_key=True, auto_created=True, verbose_name='ID', serialize=False)),
                ('name', models.CharField(unique=True, max_length=255)),
                ('slug', models.SlugField()),
            ],
            options={
                'ordering': ['name'],
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Developer',
            fields=[
                ('id', models.AutoField(primary_key=True, auto_created=True, verbose_name='ID', serialize=False)),
                ('name', models.CharField(unique=True, max_length=255)),
                ('slug', models.SlugField()),
                ('email', models.EmailField(max_length=75)),
            ],
            options={
                'ordering': ['name'],
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Game',
            fields=[
                ('id', models.AutoField(primary_key=True, auto_created=True, verbose_name='ID', serialize=False)),
                ('name', models.CharField(unique=True, max_length=255)),
                ('slug', models.SlugField()),
                ('description', models.TextField()),
                ('url', models.URLField()),
                ('image_url', models.URLField(blank=True, default='')),
                ('categories', models.ManyToManyField(related_name='category_games', to='games.Category')),
                ('developer', models.ForeignKey(related_name='developers_games', to='games.Developer')),
            ],
            options={
                'ordering': ['name'],
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Ownership',
            fields=[
                ('id', models.AutoField(primary_key=True, auto_created=True, verbose_name='ID', serialize=False)),
                ('highscore', models.PositiveIntegerField(default=0)),
                ('rating', models.PositiveIntegerField(choices=[(1, 1), (2, 2), (3, 3), (4, 4), (5, 5)])),
                ('game', models.ForeignKey(to='games.Game')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Player',
            fields=[
                ('id', models.AutoField(primary_key=True, auto_created=True, verbose_name='ID', serialize=False)),
                ('name', models.CharField(unique=True, max_length=255)),
                ('slug', models.SlugField()),
                ('email', models.EmailField(max_length=75)),
            ],
            options={
                'ordering': ['name'],
            },
            bases=(models.Model,),
        ),
        migrations.AddField(
            model_name='ownership',
            name='player',
            field=models.ForeignKey(related_name='ownerships', to='games.Player'),
            preserve_default=True,
        ),
    ]
