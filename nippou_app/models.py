# Create your models here.
from django.db import models
from datetime import datetime
from django.contrib.auth.models import AbstractUser
from django.contrib.auth.models import (
    BaseUserManager, AbstractBaseUser
)

class Task(models.Model):
    task_name = models.CharField(max_length=512)
    time_yotei = models.IntegerField()
    time_jitsu = models.IntegerField()
    task_y = models.TextField()
    task_w = models.TextField()
    task_t = models.TextField()

"""
class User(models.Model):
    user_name = models.CharField(max_length=512)
    user_pass = models.CharField(max_length=20)
    user_dev = models.CharField(max_length=512)
"""
class User(AbstractUser):
    user_dev = models.CharField(max_length=512)


class nippou_data(models.Model):
    user = models.ForeignKey(User)
    title = models.CharField(max_length=512)
    text = models.TextField()
    date = models.DateTimeField(default=datetime.now)
    task = models.ForeignKey(Task)

    #class Meta:
    #    db_table = 'nippou_data'
    #