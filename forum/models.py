from django.db import models
from django.contrib.auth.models import User
from djangotoolbox.fields import ListField,EmbeddedModelField
from auth.models import Skill
# Create your models here.


class Answer(models.Model):
	id = models.AutoField(primary_key = True)
	author = models.OneToOneField(User)
	publishedDate = models.CharField(max_length=128)
	likes = ListField(EmbeddedModelField(User))
	answerText = models.TextField()
	comments = ListField(EmbeddedModelField('Comment'))
	isAccepted = models.IntegerField()


class Comment(models.Model):

	id = models.AutoField(primary_key = True)
	author = models.OneToOneField(User)
	publishedDate = models.CharField(max_length=128)
	likes = models.IntegerField()
	commentText = models.TextField()

class Thread(models.Model):

	id = models.AutoField(primary_key = True)
	title = models.CharField(max_length=128)
	author = models.OneToOneField(User)
	publishedDate = models.CharField(max_length=128)
	questionText = models.TextField()
	answers = ListField(EmbeddedModelField('Answer'))
	likes = ListField(EmbeddedModelField(User))
	tags = ListField(EmbeddedModelField(Skill))
	comments = ListField(EmbeddedModelField('Comment'))
