
from django.db import models
from django.contrib.auth.models import User																																																																																																																																																																				
# Create your models here.
from djangotoolbox.fields import ListField,EmbeddedModelField
from django.core import serializers
from auth.models import Skill
from django_mongodb_engine.contrib import MongoDBManager


class Document(models.Model):
	document = models.FileField(upload_to='documents')
	documentName = models.CharField(max_length=100)

    

class Project(models.Model):
    user = models.OneToOneField(User)
    fileList=ListField(EmbeddedModelField(Document))
    projectName = models.TextField(max_length=50)
    skillList = ListField(EmbeddedModelField(Skill))
    branchList = ListField(models.IntegerField(default=0))
    projectDescription = models.TextField(max_length=50)
    contributorList = ListField(EmbeddedModelField(User))
    publishedDate = models.CharField(max_length=128)
    objects = MongoDBManager()
    avgRating = models.FloatField(default=0.0)
    ratingCount = models.IntegerField(default=0)
    ratings = ListField(EmbeddedModelField('Rating'))
    shortDesc = models.CharField(max_length=25)
    projectImage = models.FileField(upload_to='media/projectImage')

    def __str__(self):
            return self.projectName

class Rating(models.Model):
    user = models.OneToOneField(User,related_name='+')
    project = models.OneToOneField(Project,related_name='+')
    rating = models.FloatField()
