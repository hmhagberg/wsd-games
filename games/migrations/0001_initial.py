# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings
import django.core.validators
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('auth', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='WsdGamesUser',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(default=django.utils.timezone.now, verbose_name='last login')),
                ('is_superuser', models.BooleanField(default=False, help_text='Designates that this user has all permissions without explicitly assigning them.', verbose_name='superuser status')),
                ('username', models.CharField(unique=True, verbose_name='username', max_length=30, help_text='Required. 30 characters or fewer. Letters, digits and @/./+/-/_ only.', validators=[django.core.validators.RegexValidator('^[\\w.@+-]+$', 'Enter a valid username.', 'invalid')])),
                ('first_name', models.CharField(blank=True, max_length=30, verbose_name='first name')),
                ('last_name', models.CharField(blank=True, max_length=30, verbose_name='last name')),
                ('email', models.EmailField(blank=True, max_length=75, verbose_name='email address')),
                ('is_staff', models.BooleanField(default=False, help_text='Designates whether the user can log into this admin site.', verbose_name='staff status')),
                ('is_active', models.BooleanField(default=True, help_text='Designates whether this user should be treated as active. Unselect this instead of deleting accounts.', verbose_name='active')),
                ('date_joined', models.DateTimeField(default=django.utils.timezone.now, verbose_name='date joined')),
                ('api_token', models.CharField(unique=True, max_length=40)),
                ('groups', models.ManyToManyField(blank=True, related_name='user_set', help_text='The groups this user belongs to. A user will get all permissions granted to each of his/her group.', related_query_name='user', to='auth.Group', verbose_name='groups')),
                ('user_permissions', models.ManyToManyField(blank=True, related_name='user_set', help_text='Specific permissions for this user.', related_query_name='user', to='auth.Permission', verbose_name='user permissions')),
            ],
            options={
                'abstract': False,
                'verbose_name_plural': 'users',
                'verbose_name': 'user',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
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
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
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
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(unique=True, max_length=255)),
                ('slug', models.SlugField()),
                ('description', models.TextField(default='Game description')),
                ('url', models.URLField()),
                ('image_url', models.URLField(default='http://rammb.cira.colostate.edu/dev/hillger/WSD_logo.gif', blank=True)),
                ('price', models.DecimalField(max_digits=6, decimal_places=2)),
                ('categories', models.ManyToManyField(related_name='games', to='games.Category')),
                ('developer', models.ForeignKey(related_name='games', to='games.Developer')),
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
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('highscore', models.PositiveIntegerField(default=0)),
                ('saved_score', models.PositiveIntegerField(default=0)),
                ('saved_data', models.TextField(default='[]')),
                ('rating', models.PositiveIntegerField(null=True, choices=[(1, 1), (2, 2), (3, 3), (4, 4), (5, 5)])),
                ('game', models.ForeignKey(related_name='ownerships', to='games.Game')),
            ],
            options={
                'ordering': ['-highscore'],
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Payment',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('completed', models.BooleanField(default=False)),
                ('timestamp', models.DateTimeField(auto_now_add=True)),
                ('pid', models.CharField(unique=True, max_length=32)),
                ('ref', models.CharField(blank=True, max_length=32)),
                ('game', models.ForeignKey(related_name='sales', to='games.Game')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Player',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
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
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
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
            field=models.ForeignKey(related_name='payments', to='games.Player'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='ownership',
            name='player',
            field=models.ForeignKey(related_name='ownerships', to='games.Player'),
            preserve_default=True,
        ),
    ]
