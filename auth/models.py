from django.db import models
from djangotoolbox.fields import ListField,EmbeddedModelField
from django.contrib.auth.models import User

# Create your models here.
class Skill(models.Model):
	id = models.AutoField(primary_key=True)
	skillName = models.CharField(max_length=50)

	def __str__(self):
		return self.skillName

class profilePic:
	picFile = models.FileField(upload_to='documents',default=None,null=True)
	#picName = models.charField(max_length=50)

class UserProfile(models.Model):
	user = models.OneToOneField(User,on_delete=models.CASCADE,primary_key=True)
	regNum = models.CharField(max_length=10)
	branch = models.CharField(max_length=2)
	level = models.CharField(max_length=2)
	skillList = ListField(EmbeddedModelField('Skill'))
	phoneNo = models.CharField(max_length=11)
	shareNo = models.CharField(max_length=1)
	MOOCList = ListField()
	researchPaperList = ListField()
	aboutMe = models.CharField(max_length=100)
	conferenceList = ListField()
	profilePicture = ListField(EmbeddedModelField('profilePic'))
	notify = models.IntegerField(default=0)
	def __str__(self):
		return self.regNum
