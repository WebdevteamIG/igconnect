from django.db import models
from djangotoolbox.fields import ListField,EmbeddedModelField
from django.contrib.auth.models import User

# Create your models here.


class Message(models.Model):
    receiver = models.OneToOneField(User,on_delete=models.CASCADE,related_name='+')
    sender = models.OneToOneField(User,on_delete=models.CASCADE,related_name='+')
    body = models.TextField()
    time = models.TextField()


class Chat(models.Model):
    id = models.AutoField(primary_key=True)
    receiver = models.OneToOneField(User,on_delete=models.CASCADE,related_name='+')
    sender = models.OneToOneField(User,on_delete=models.CASCADE,related_name='+')
    messages = ListField(EmbeddedModelField('Message'))
    notify = models.IntegerField(default=0)
    time = models.CharField(max_length=100)    