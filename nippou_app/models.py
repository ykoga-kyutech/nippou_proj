# Create your models here.
from django.db import models
from datetime import datetime

class nippou_data(models.Model):
    title = models.CharField(max_length=512)
    text = models.TextField()
    date = models.DateTimeField(default=datetime.now)

    #class Meta:
    #    db_table = 'nippou_data'
    #
