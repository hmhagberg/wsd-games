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
                ('id', models.AutoField(primary_key=True, verbose_name='ID', auto_created=True, serialize=False)),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(verbose_name='last login', default=django.utils.timezone.now)),
                ('is_superuser', models.BooleanField(help_text='Designates that this user has all permissions without explicitly assigning them.', verbose_name='superuser status', default=False)),
                ('username', models.CharField(max_length=30, help_text='Required. 30 characters or fewer. Letters, digits and @/./+/-/_ only.', verbose_name='username', unique=True, validators=[django.core.validators.RegexValidator('^[\\w.@+-]+$', 'Enter a valid username.', 'invalid')])),
                ('first_name', models.CharField(blank=True, max_length=30, verbose_name='first name')),
                ('last_name', models.CharField(blank=True, max_length=30, verbose_name='last name')),
                ('email', models.EmailField(blank=True, max_length=75, verbose_name='email address')),
                ('is_staff', models.BooleanField(help_text='Designates whether the user can log into this admin site.', verbose_name='staff status', default=False)),
                ('is_active', models.BooleanField(help_text='Designates whether this user should be treated as active. Unselect this instead of deleting accounts.', verbose_name='active', default=True)),
                ('date_joined', models.DateTimeField(verbose_name='date joined', default=django.utils.timezone.now)),
                ('groups', models.ManyToManyField(blank=True, related_query_name='user', help_text='The groups this user belongs to. A user will get all permissions granted to each of his/her group.', related_name='user_set', to='auth.Group', verbose_name='groups')),
                ('user_permissions', models.ManyToManyField(blank=True, related_query_name='user', help_text='Specific permissions for this user.', related_name='user_set', to='auth.Permission', verbose_name='user permissions')),
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
                ('id', models.AutoField(primary_key=True, verbose_name='ID', auto_created=True, serialize=False)),
                ('name', models.CharField(max_length=255, unique=True)),
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
                ('id', models.AutoField(primary_key=True, verbose_name='ID', auto_created=True, serialize=False)),
                ('name', models.CharField(max_length=255, unique=True)),
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
                ('id', models.AutoField(primary_key=True, verbose_name='ID', auto_created=True, serialize=False)),
                ('name', models.CharField(max_length=255, unique=True)),
                ('slug', models.SlugField()),
                ('description', models.TextField(default='Game description')),
                ('url', models.URLField()),
                ('image_url', models.URLField(blank=True, default='http://rammb.cira.colostate.edu/dev/hillger/WSD_logo.gif')),
                ('price', models.DecimalField(max_digits=6, decimal_places=2)),
                ('categories', models.ManyToManyField(related_name='category_games', to='games.Category')),
                ('developer', models.ForeignKey(related_name='developers_games', to='games.Developer')),
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
                ('id', models.AutoField(primary_key=True, verbose_name='ID', auto_created=True, serialize=False)),
                ('highscore', models.PositiveIntegerField(default=0)),
                ('saved_score', models.PositiveIntegerField(default=0)),
                ('saved_data', models.TextField(default='[]')),
                ('rating', models.PositiveIntegerField(choices=[(1, 1), (2, 2), (3, 3), (4, 4), (5, 5)], null=True)),
                ('payment_timestamp', models.DateTimeField(auto_now_add=True)),
                ('payment_completed', models.BooleanField(default=False)),
                ('payment_pid', models.CharField(max_length=32, unique=True)),
                ('payment_ref', models.CharField(blank=True, max_length=32)),
                ('game', models.ForeignKey(related_name='ownerships', to='games.Game')),
            ],
            options={
                'ordering': ['-highscore'],
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Player',
            fields=[
                ('id', models.AutoField(primary_key=True, verbose_name='ID', auto_created=True, serialize=False)),
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
                ('id', models.AutoField(primary_key=True, verbose_name='ID', auto_created=True, serialize=False)),
                ('key', models.CharField(max_length=32, unique=True, default='ebd03905361842b4a46ac8810b8bb2b4')),
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
            field=models.ForeignKey(related_name='ownerships', to='games.Player'),
            preserve_default=True,
        ),
    ]
