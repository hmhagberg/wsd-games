# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings
import datetime
import django.utils.timezone
import django.core.validators


class Migration(migrations.Migration):

    dependencies = [
        ('auth', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='WsdGamesUser',
            fields=[
                ('id', models.AutoField(serialize=False, auto_created=True, verbose_name='ID', primary_key=True)),
                ('password', models.CharField(verbose_name='password', max_length=128)),
                ('last_login', models.DateTimeField(verbose_name='last login', default=django.utils.timezone.now)),
                ('is_superuser', models.BooleanField(verbose_name='superuser status', help_text='Designates that this user has all permissions without explicitly assigning them.', default=False)),
                ('username', models.CharField(validators=[django.core.validators.RegexValidator('^[\\w.@+-]+$', 'Enter a valid username.', 'invalid')], verbose_name='username', max_length=30, unique=True, help_text='Required. 30 characters or fewer. Letters, digits and @/./+/-/_ only.')),
                ('first_name', models.CharField(max_length=30, verbose_name='first name', blank=True)),
                ('last_name', models.CharField(max_length=30, verbose_name='last name', blank=True)),
                ('email', models.EmailField(max_length=75, verbose_name='email address', blank=True)),
                ('is_staff', models.BooleanField(verbose_name='staff status', help_text='Designates whether the user can log into this admin site.', default=False)),
                ('is_active', models.BooleanField(verbose_name='active', help_text='Designates whether this user should be treated as active. Unselect this instead of deleting accounts.', default=True)),
                ('date_joined', models.DateTimeField(verbose_name='date joined', default=django.utils.timezone.now)),
                ('api_token', models.CharField(unique=True, max_length=40)),
                ('groups', models.ManyToManyField(verbose_name='groups', help_text='The groups this user belongs to. A user will get all permissions granted to each of his/her group.', to='auth.Group', blank=True, related_query_name='user', related_name='user_set')),
                ('user_permissions', models.ManyToManyField(verbose_name='user permissions', help_text='Specific permissions for this user.', to='auth.Permission', blank=True, related_query_name='user', related_name='user_set')),
            ],
            options={
                'verbose_name': 'user',
                'verbose_name_plural': 'users',
                'abstract': False,
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.AutoField(serialize=False, auto_created=True, verbose_name='ID', primary_key=True)),
                ('name', models.CharField(unique=True, max_length=255)),
                ('slug', models.SlugField()),
                ('image_url', models.URLField(blank=True, default='http://rammb.cira.colostate.edu/dev/hillger/WSD_logo.gif')),
                ('description', models.TextField(default='Category description')),
            ],
            options={
                'ordering': ['name'],
                'abstract': False,
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Developer',
            fields=[
                ('id', models.AutoField(serialize=False, auto_created=True, verbose_name='ID', primary_key=True)),
                ('name', models.CharField(unique=True, max_length=255)),
                ('slug', models.SlugField()),
                ('image_url', models.URLField(blank=True, default='http://rammb.cira.colostate.edu/dev/hillger/WSD_logo.gif')),
                ('description', models.TextField(default='Developer description')),
                ('user', models.OneToOneField(to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'ordering': ['name'],
                'abstract': False,
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Game',
            fields=[
                ('id', models.AutoField(serialize=False, auto_created=True, verbose_name='ID', primary_key=True)),
                ('name', models.CharField(unique=True, max_length=255)),
                ('slug', models.SlugField()),
                ('description', models.TextField(default='Game description')),
                ('url', models.URLField()),
                ('image_url', models.URLField(blank=True, default='http://rammb.cira.colostate.edu/dev/hillger/WSD_logo.gif')),
                ('price', models.DecimalField(max_digits=6, validators=[django.core.validators.MinValueValidator(0.01)], decimal_places=2)),
                ('publish_date', models.DateField(auto_now_add=True, default=datetime.date(2015, 2, 12))),
                ('categories', models.ManyToManyField(to='games.Category', related_name='games')),
                ('developer', models.ForeignKey(to='games.Developer', related_name='games')),
            ],
            options={
                'ordering': ['name'],
                'abstract': False,
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Ownership',
            fields=[
                ('id', models.AutoField(serialize=False, auto_created=True, verbose_name='ID', primary_key=True)),
                ('highscore', models.PositiveIntegerField(default=0)),
                ('saved_score', models.PositiveIntegerField(default=0)),
                ('saved_data', models.TextField(default='[]')),
                ('rating', models.PositiveIntegerField(null=True, choices=[(1, 1), (2, 2), (3, 3), (4, 4), (5, 5)])),
                ('timestamp', models.DateTimeField(auto_now_add=True, default=datetime.datetime(2015, 2, 12, 13, 28, 6, 27600))),
                ('game', models.ForeignKey(to='games.Game', related_name='ownerships')),
            ],
            options={
                'ordering': ['-highscore'],
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Payment',
            fields=[
                ('id', models.AutoField(serialize=False, auto_created=True, verbose_name='ID', primary_key=True)),
                ('completed', models.BooleanField(default=False)),
                ('timestamp', models.DateTimeField(auto_now_add=True)),
                ('pid', models.CharField(unique=True, max_length=32)),
                ('ref', models.CharField(max_length=32, blank=True)),
                ('game', models.ForeignKey(to='games.Game', related_name='sales')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Player',
            fields=[
                ('id', models.AutoField(serialize=False, auto_created=True, verbose_name='ID', primary_key=True)),
                ('slug', models.SlugField()),
                ('about_me', models.TextField(blank=True)),
                ('user', models.OneToOneField(to=settings.AUTH_USER_MODEL)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='SignupActivation',
            fields=[
                ('id', models.AutoField(serialize=False, auto_created=True, verbose_name='ID', primary_key=True)),
                ('key', models.CharField(unique=True, max_length=32)),
                ('time_sent', models.DateTimeField(auto_now_add=True)),
                ('user', models.OneToOneField(to=settings.AUTH_USER_MODEL)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.AddField(
            model_name='payment',
            name='player',
            field=models.ForeignKey(to='games.Player', related_name='payments'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='ownership',
            name='player',
            field=models.ForeignKey(to='games.Player', related_name='ownerships'),
            preserve_default=True,
        ),
    ]
