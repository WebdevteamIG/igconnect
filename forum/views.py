# Create your views here.
from django.shortcuts import render,redirect
from django.http import HttpResponse
from django.shortcuts import get_object_or_404,render
from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from dashboard.models import Project,Document
from auth.models import Skill
from forum.models import Answer,Thread,Comment
import json,os
from djangotoolbox.fields import ListField,EmbeddedModelField
from dashboard.forms import DocumentForm
from datetime import datetime




def createThread(request):
	if not request.user.is_authenticated() or not request.user.is_active :
		return redirect('/auth/')

	if not request.method == 'POST' :
		data = {
			'user' : request.user,
			'skills' : Skill.objects.all()
		}
		return render(request,'forum/createNew.html',data)

	requestReceived=json.loads(request.POST.get("thread"))
	json.dumps(requestReceived)
	threadTitle=requestReceived['threadTitle']
	threadQuestion=requestReceived['threadQuestion']
	skills=requestReceived['tags']
	tagList=[]
	currentTimeStamp = datetime.strftime(datetime.now(), '%Y-%m-%d %H:%M')
	for skillId in skills:
		skill=Skill.objects.get(id=skillId)
		tagList.append(skill)
		print skill.skillName
	
	thread=Thread(title=threadTitle,author=request.user,publishedDate = currentTimeStamp,tags=tagList,questionText=threadQuestion)
	thread.save()
	return HttpResponse()


def viewAllThreads(request):
	if not request.user.is_authenticated() or not request.user.is_active :
		return redirect('/auth/')

	threads = Thread.objects.all()
	data = {
		'user' : request.user,
		'threads' : threads,
	}
	return render(request,'forum/allThreads.html',data)

def viewThread(request):
	if not request.user.is_authenticated() or not request.user.is_active :
		return redirect('/auth/')
	if request.method == 'GET':
		threadId = request.GET.get('threadId')
		thread = Thread.objects.get(id = threadId)
		data={
			'thread' : thread,
			'user' : request.user
		}
		return render(request,'forum/viewThread.html',data)	