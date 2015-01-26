# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.utils.timezone
from django.conf import settings
import django.core.validators


class Migration(migrations.Migration):

    dependencies = [
        ('auth', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='WsdGamesUser',
            fields=[
                ('id', models.AutoField(serialize=False, verbose_name='ID', auto_created=True, primary_key=True)),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(default=django.utils.timezone.now, verbose_name='last login')),
                ('is_superuser', models.BooleanField(default=False, verbose_name='superuser status', help_text='Designates that this user has all permissions without explicitly assigning them.')),
                ('username', models.CharField(max_length=30, verbose_name='username', unique=True, help_text='Required. 30 characters or fewer. Letters, digits and @/./+/-/_ only.', validators=[django.core.validators.RegexValidator('^[\\w.@+-]+$', 'Enter a valid username.', 'invalid')])),
                ('first_name', models.CharField(max_length=30, verbose_name='first name', blank=True)),
                ('last_name', models.CharField(max_length=30, verbose_name='last name', blank=True)),
                ('email', models.EmailField(max_length=75, verbose_name='email address', blank=True)),
                ('is_staff', models.BooleanField(default=False, verbose_name='staff status', help_text='Designates whether the user can log into this admin site.')),
                ('is_active', models.BooleanField(default=True, verbose_name='active', help_text='Designates whether this user should be treated as active. Unselect this instead of deleting accounts.')),
                ('date_joined', models.DateTimeField(default=django.utils.timezone.now, verbose_name='date joined')),
                ('groups', models.ManyToManyField(to='auth.Group', help_text='The groups this user belongs to. A user will get all permissions granted to each of his/her group.', related_query_name='user', verbose_name='groups', related_name='user_set', blank=True)),
                ('user_permissions', models.ManyToManyField(to='auth.Permission', help_text='Specific permissions for this user.', related_query_name='user', verbose_name='user permissions', related_name='user_set', blank=True)),
            ],
            options={
                'verbose_name_plural': 'users',
                'verbose_name': 'user',
                'abstract': False,
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.AutoField(serialize=False, verbose_name='ID', auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=255, unique=True)),
                ('slug', models.SlugField()),
                ('image_url', models.URLField(default='http://rammb.cira.colostate.edu/dev/hillger/WSD_logo.gif', blank=True)),
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
                ('id', models.AutoField(serialize=False, verbose_name='ID', auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=255, unique=True)),
                ('slug', models.SlugField()),
                ('image_url', models.URLField(default='http://rammb.cira.colostate.edu/dev/hillger/WSD_logo.gif', blank=True)),
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
                ('id', models.AutoField(serialize=False, verbose_name='ID', auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=255, unique=True)),
                ('slug', models.SlugField()),
                ('description', models.TextField(default='Game description')),
                ('url', models.URLField()),
                ('image_url', models.URLField(default='http://rammb.cira.colostate.edu/dev/hillger/WSD_logo.gif', blank=True)),
                ('price', models.DecimalField(decimal_places=2, max_digits=6)),
                ('categories', models.ManyToManyField(to='games.Category', related_name='category_games')),
                ('developer', models.ForeignKey(to='games.Developer', related_name='developers_games')),
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
                ('id', models.AutoField(serialize=False, verbose_name='ID', auto_created=True, primary_key=True)),
                ('highscore', models.PositiveIntegerField(default=0)),
                ('saved_score', models.PositiveIntegerField(default=0)),
                ('saved_data', models.TextField(default='[]')),
                ('rating', models.PositiveIntegerField(choices=[(1, 1), (2, 2), (3, 3), (4, 4), (5, 5)], null=True)),
                ('payment_timestamp', models.DateTimeField(auto_now_add=True)),
                ('payment_completed', models.BooleanField(default=False)),
                ('payment_pid', models.CharField(max_length=32, unique=True)),
                ('payment_ref', models.CharField(max_length=32, blank=True)),
                ('game', models.ForeignKey(to='games.Game', related_name='ownerships')),
            ],
            options={
                'ordering': ['-highscore'],
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Player',
            fields=[
                ('id', models.AutoField(serialize=False, verbose_name='ID', auto_created=True, primary_key=True)),
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
                ('id', models.AutoField(serialize=False, verbose_name='ID', auto_created=True, primary_key=True)),
                ('key', models.CharField(default='59513af93fdc4c52939ca4d607aa0ece', max_length=32, unique=True)),
                ('time_sent', models.DateTimeField(auto_now_add=True)),
                ('user', models.OneToOneField(to=settings.AUTH_USER_MODEL)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.AddField(
            model_name='ownership',
            name='player',
            field=models.ForeignKey(to='games.Player', related_name='ownerships'),
            preserve_default=True,
        ),
    ]
