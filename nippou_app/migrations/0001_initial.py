# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.utils.timezone
import datetime
import django.contrib.auth.models
from django.conf import settings
import django.core.validators


class Migration(migrations.Migration):

    dependencies = [
        ('auth', '0006_require_contenttypes_0002'),
    ]

    operations = [
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.AutoField(auto_created=True, verbose_name='ID', primary_key=True, serialize=False)),
                ('password', models.CharField(verbose_name='password', max_length=128)),
                ('last_login', models.DateTimeField(verbose_name='last login', null=True, blank=True)),
                ('is_superuser', models.BooleanField(default=False, help_text='Designates that this user has all permissions without explicitly assigning them.', verbose_name='superuser status')),
                ('username', models.CharField(help_text='Required. 30 characters or fewer. Letters, digits and @/./+/-/_ only.', max_length=30, validators=[django.core.validators.RegexValidator('^[\\w.@+-]+$', 'Enter a valid username. This value may contain only letters, numbers and @/./+/-/_ characters.', 'invalid')], verbose_name='username', error_messages={'unique': 'A user with that username already exists.'}, unique=True)),
                ('first_name', models.CharField(verbose_name='first name', max_length=30, blank=True)),
                ('last_name', models.CharField(verbose_name='last name', max_length=30, blank=True)),
                ('email', models.EmailField(verbose_name='email address', max_length=254, blank=True)),
                ('is_staff', models.BooleanField(default=False, help_text='Designates whether the user can log into this admin site.', verbose_name='staff status')),
                ('is_active', models.BooleanField(default=True, help_text='Designates whether this user should be treated as active. Unselect this instead of deleting accounts.', verbose_name='active')),
                ('date_joined', models.DateTimeField(default=django.utils.timezone.now, verbose_name='date joined')),
                ('user_dev', models.CharField(max_length=512)),
                ('groups', models.ManyToManyField(to='auth.Group', help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.', blank=True, related_query_name='user', verbose_name='groups', related_name='user_set')),
                ('user_permissions', models.ManyToManyField(to='auth.Permission', help_text='Specific permissions for this user.', blank=True, related_query_name='user', verbose_name='user permissions', related_name='user_set')),
            ],
            options={
                'abstract': False,
                'verbose_name': 'user',
                'verbose_name_plural': 'users',
            },
            managers=[
                ('objects', django.contrib.auth.models.UserManager()),
            ],
        ),
        migrations.CreateModel(
            name='nippou_data',
            fields=[
                ('id', models.AutoField(auto_created=True, verbose_name='ID', primary_key=True, serialize=False)),
                ('title', models.CharField(max_length=512)),
                ('text', models.TextField()),
                ('date', models.DateTimeField(default=datetime.datetime.now)),
            ],
        ),
        migrations.CreateModel(
            name='Task',
            fields=[
                ('id', models.AutoField(auto_created=True, verbose_name='ID', primary_key=True, serialize=False)),
                ('task_name', models.CharField(max_length=512)),
                ('time_yotei', models.IntegerField()),
                ('time_jitsu', models.IntegerField()),
                ('task_y', models.TextField()),
                ('task_w', models.TextField()),
                ('task_t', models.TextField()),
            ],
        ),
        migrations.AddField(
            model_name='nippou_data',
            name='task',
            field=models.ForeignKey(to='nippou_app.Task'),
        ),
        migrations.AddField(
            model_name='nippou_data',
            name='user',
            field=models.ForeignKey(to=settings.AUTH_USER_MODEL),
        ),
    ]
