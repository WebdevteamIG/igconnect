

from django.http import HttpResponse
from django.shortcuts import get_object_or_404,render,redirect
from django.contrib.auth import authenticate,login
from django.contrib.auth import logout
from django.contrib.auth.models import User
from auth.models import Skill
from djangotoolbox.fields import ListField,EmbeddedModelField
from dashboard.forms import DocumentForm
from datetime import datetime
from django.core.paginator import Paginator
from .models import Event
import json,os,pymongo
from django.core.serializers.json import DjangoJSONEncoder
from bson.json_util import dumps
from django.core import serializers
from django.db.models import Q
from django.views.decorators.csrf import csrf_exempt, csrf_protect
# Create your views here.

client = pymongo.MongoClient('0.0.0.0', 27017)
db = client.igconnect_db
@csrf_exempt
def index(request,pageNo=None):

    return redirect('/event/viewall')


def addEvent(request):
    if not  request.user.is_authenticated() or not request.user.is_active == True:
		redirect("/auth/")
    if request.method=="POST":
        requestReceived=json.loads(request.POST.get("event"))
        json.dumps(requestReceived)
        eventName=requestReceived['eventname']
        eventDescription=requestReceived['eventDescription']
        organiser=requestReceived['organiser']
        skills=requestReceived['skills']
        sdate=requestReceived['startdate']
        edate=requestReceived['enddate']
        skillList=[]
        for skillId in skills:
            skill=Skill.objects.get(id=skillId)
            skillList.append(skill)

        mentors=requestReceived['mentors']
        mentorList=[]
        for username in mentors:
            user=User.objects.get(username=username)
            mentorList.append(user)
        event=Event(user=request.user,eventName=eventName,startdate=sdate,enddate=edate,description=eventDescription,organiser=organiser,mentorList=mentorList,skillList=skillList)
        event.save()
        return HttpResponse()


    else:

		users=User.objects.all();
		skills=Skill.objects.all();
		if request.user.is_authenticated():
			return render(request,'event/addevent.html',{'skills':skills,'users':users,'username':request.user.username});	
		else:
			return redirect("/auth/")
@csrf_exempt
def viewall(request,pageNo=None):
    if request.user.is_authenticated() and request.user.is_active == True:
        eventList=Event.objects.order_by('eventName')
        paginator = Paginator(eventList,3)
        
        if request.method == 'POST':
            print "hi"
            data = json.loads(request.POST['data'])
            json.dumps(data)
            print "see u again"
            return categorise(data)

        if pageNo is None: 
            events = paginator.page(1)
            eventList = events.object_list
            myevents = list()
            for event in eventList:
                myUser = {
                    'first_name':event.user.first_name,
                    'last_name':event.user.last_name
                }

                myEvent = {
                    'startdate':event.startdate,
                    'enddate':event.enddate,
                    'id':event.id,
                    'user':myUser,
                    'eventName':event.eventName,
                    'eventDescription':event.description,
                    'skillList':event.skillList,
                    'mentorList':event.mentorList,

                }

                myevents.append(myEvent)
            users=User.objects.all()
            return render(request,'event/showevent.html',{'events':myevents,'username':request.user.username,'users':users})
        else:
            events = paginator.page(pageNo)
            eventList = events.object_list
            myevents = list()
            for event in eventList:
                myUser = {
                    'first_name':event.user.first_name,
                    'last_name':event.user.last_name
                }
                skills = []
                for skill in event.skillList:
                    skills.append(skill.skillName)
                mentors = []
                for men in event.mentorList:
                    mentors.append({'first_name':men.first_name,})
                sd = json.dumps(event.startdate, cls=DjangoJSONEncoder)
                ed = json.dumps(event.enddate, cls=DjangoJSONEncoder)
                myEvent = {
                    'startdate':sd,
                    'enddate':ed,
                    'id':event.id,
                    'user':myUser,
                    'eventName':event.eventName,
                    'eventDescription':event.description,
                    'skillList':skills,
                    'mentorList':mentors,
                }
                myevents.append(myEvent)

            return HttpResponse(json.dumps(myevents),mimetype="application/json")
    else:
        return redirect("/auth/")


@csrf_exempt
def categorise(data):
    eventList = set()
    times = [int(x) for x in data['eventList']]
    events=[]
    x = datetime.now()
    x = x.strftime("%Y-%m-%d")
    upevents=[]
    pastevents=[]
    todayevents=[]
#    print x
#    print "hello"
    e = Event.objects.all()
    for event in e:
        if 1 in times:
            if(event.startdate.strftime("%Y-%m-%d") > x):
                upevents.append(event)
#                print "upcoming"
        if 2 in times:
            if(event.startdate.strftime("%Y-%m-%d") < x):
                pastevents.append(event)
#                print "past"
        if 3 in times:
            if(event.startdate.strftime("%Y-%m-%d") == x):
                todayevents.append(event)
#                print "today"
    
    events=[]
    events=upevents+pastevents+todayevents
    print events
    print data['pageNo']
    paginator = Paginator(events,3)
    eventList = paginator.page(data['pageNo'])
    eventList = eventList.object_list
    myEvents = []
#    print "lollllllz"
    for event in eventList:
        myUser = {
            'first_name':event.user.first_name,
            'last_name':event.user.last_name
        }
        skills = []
        for skill in event.skillList:
            skills.append(skill.skillName)
        mentors = []
        for men in event.mentorList:
            mentors.append({'first_name':men.first_name,})
        sd = json.dumps(event.startdate, cls=DjangoJSONEncoder)
        ed = json.dumps(event.enddate, cls=DjangoJSONEncoder)
        myEvent = {
            'startdate':sd,
            'enddate':ed,
            'id':event.id,
            'user':myUser,
            'eventName':event.eventName,
            'eventDescription':event.description,
            'skillList':skills,
            'mentorList':mentors,
        }
        myEvents.append(myEvent)
#    print "lol"
    return HttpResponse(json.dumps(myEvents),mimetype="application/json")


