# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='nippou_data',
            fields=[
                ('id', models.AutoField(primary_key=True, verbose_name='ID', auto_created=True, serialize=False)),
                ('title', models.CharField(max_length=512)),
                ('text', models.TextField()),
                ('date', models.DateTimeField(default=datetime.datetime.now)),
            ],
        ),
        migrations.CreateModel(
            name='Task',
            fields=[
                ('id', models.AutoField(primary_key=True, verbose_name='ID', auto_created=True, serialize=False)),
                ('task_name', models.CharField(max_length=512)),
                ('time_yotei', models.IntegerField()),
                ('time_jitsu', models.IntegerField()),
                ('task_y', models.TextField()),
                ('task_w', models.TextField()),
                ('task_t', models.TextField()),
            ],
        ),
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.AutoField(primary_key=True, verbose_name='ID', auto_created=True, serialize=False)),
                ('user_name', models.CharField(max_length=512)),
                ('user_pass', models.CharField(max_length=20)),
                ('user_dev', models.CharField(max_length=512)),
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
            field=models.ForeignKey(to='nippou_app.User'),
        ),
    ]
