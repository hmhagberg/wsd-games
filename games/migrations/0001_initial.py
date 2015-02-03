# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.core.validators
from django.conf import settings
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('auth', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='WsdGamesUser',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, verbose_name='ID', serialize=False)),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(default=django.utils.timezone.now, verbose_name='last login')),
                ('is_superuser', models.BooleanField(help_text='Designates that this user has all permissions without explicitly assigning them.', default=False, verbose_name='superuser status')),
                ('username', models.CharField(help_text='Required. 30 characters or fewer. Letters, digits and @/./+/-/_ only.', unique=True, validators=[django.core.validators.RegexValidator('^[\\w.@+-]+$', 'Enter a valid username.', 'invalid')], max_length=30, verbose_name='username')),
                ('first_name', models.CharField(blank=True, max_length=30, verbose_name='first name')),
                ('last_name', models.CharField(blank=True, max_length=30, verbose_name='last name')),
                ('email', models.EmailField(blank=True, max_length=75, verbose_name='email address')),
                ('is_staff', models.BooleanField(help_text='Designates whether the user can log into this admin site.', default=False, verbose_name='staff status')),
                ('is_active', models.BooleanField(help_text='Designates whether this user should be treated as active. Unselect this instead of deleting accounts.', default=True, verbose_name='active')),
                ('date_joined', models.DateTimeField(default=django.utils.timezone.now, verbose_name='date joined')),
                ('api_token', models.CharField(unique=True, max_length=40)),
                ('groups', models.ManyToManyField(help_text='The groups this user belongs to. A user will get all permissions granted to each of his/her group.', related_query_name='user', blank=True, verbose_name='groups', to='auth.Group', related_name='user_set')),
                ('user_permissions', models.ManyToManyField(help_text='Specific permissions for this user.', related_query_name='user', blank=True, verbose_name='user permissions', to='auth.Permission', related_name='user_set')),
            ],
            options={
                'verbose_name_plural': 'users',
                'abstract': False,
                'verbose_name': 'user',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, verbose_name='ID', serialize=False)),
                ('name', models.CharField(unique=True, max_length=255)),
                ('slug', models.SlugField()),
                ('image_url', models.URLField(default='http://rammb.cira.colostate.edu/dev/hillger/WSD_logo.gif', blank=True)),
                ('description', models.TextField(default='Category description')),
            ],
            options={
                'abstract': False,
                'ordering': ['name'],
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Developer',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, verbose_name='ID', serialize=False)),
                ('name', models.CharField(unique=True, max_length=255)),
                ('slug', models.SlugField()),
                ('image_url', models.URLField(default='http://rammb.cira.colostate.edu/dev/hillger/WSD_logo.gif', blank=True)),
                ('description', models.TextField(default='Developer description')),
                ('user', models.OneToOneField(to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'abstract': False,
                'ordering': ['name'],
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Game',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, verbose_name='ID', serialize=False)),
                ('name', models.CharField(unique=True, max_length=255)),
                ('slug', models.SlugField()),
                ('description', models.TextField(default='Game description')),
                ('url', models.URLField()),
                ('image_url', models.URLField(default='http://rammb.cira.colostate.edu/dev/hillger/WSD_logo.gif', blank=True)),
                ('price', models.DecimalField(max_digits=6, decimal_places=2)),
                ('categories', models.ManyToManyField(to='games.Category', related_name='games')),
                ('developer', models.ForeignKey(to='games.Developer', related_name='games')),
            ],
            options={
                'abstract': False,
                'ordering': ['name'],
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Ownership',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, verbose_name='ID', serialize=False)),
                ('highscore', models.PositiveIntegerField(default=0)),
                ('saved_score', models.PositiveIntegerField(default=0)),
                ('saved_data', models.TextField(default='[]')),
                ('rating', models.PositiveIntegerField(null=True, choices=[(1, 1), (2, 2), (3, 3), (4, 4), (5, 5)])),
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
                ('id', models.AutoField(auto_created=True, primary_key=True, verbose_name='ID', serialize=False)),
                ('completed', models.BooleanField(default=False)),
                ('timestamp', models.DateTimeField(auto_now_add=True)),
                ('pid', models.CharField(unique=True, max_length=32)),
                ('ref', models.CharField(blank=True, max_length=32)),
                ('game', models.ForeignKey(to='games.Game', related_name='payments')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Player',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, verbose_name='ID', serialize=False)),
                ('slug', models.SlugField()),
                ('user', models.OneToOneField(to=settings.AUTH_USER_MODEL)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='SignupActivation',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, verbose_name='ID', serialize=False)),
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
