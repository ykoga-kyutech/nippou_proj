# Create your models here.
from django.db import models
from datetime import datetime
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
    user_dev = models.CharField(max_length=512)

class nippou_data(models.Model):
    user = models.ForeignKey(User)
    title = models.CharField('タイトル', max_length=512)
    text = models.TextField('本文')
    date = models.DateTimeField('投稿日時', default=datetime.now)
    open = models.BooleanField('公開', default=False)

class Task(models.Model):

    nippou = models.ForeignKey(nippou_data)
    task_name = models.CharField('タスク名', max_length=512)
    time_yotei = models.IntegerField('予定時間')
    time_jitsu = models.IntegerField('実時間')
    task_y = models.TextField('Y:やったこと')
    task_w = models.TextField('W:わかったこと')
    task_t = models.TextField('T:次やること')

"""
class User(models.Model):
    user_name = models.CharField(max_length=512)
    user_pass = models.CharField(max_length=20)
    user_dev = models.CharField(max_length=512)
"""