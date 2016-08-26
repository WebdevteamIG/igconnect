


from django.db import models
from django.contrib.auth.models import User
from djangotoolbox.fields import ListField,EmbeddedModelField
from django.core import serializers
from django_mongodb_engine.contrib import MongoDBManager
from django.utils.formats import get_format
from auth.models import Skill
# Create your models here.


class Event(models.Model):
    user = models.OneToOneField(User,on_delete=models.CASCADE)
    eventName = models.CharField(max_length=50)
    startdate = models.DateField()
    enddate = models.DateField()
    description = models.CharField(max_length=50)
    organiser = models.CharField(max_length=50)
    mentorList = ListField(EmbeddedModelField(User))
    skillList = ListField(EmbeddedModelField(Skill))
    
    def __str__(self):
        return self.eventName
