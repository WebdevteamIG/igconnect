

from django.shortcuts import render,redirect
from django.http import HttpResponse
from dashboard.models import Project
from event.models import Event
import pymongo,json
from bson.json_util import dumps

# Create your views here.

client = pymongo.MongoClient('0.0.0.0', 27017)
db = client.igconnect_db

def index(request):
	if request.user.is_authenticated() == True and request.user.is_active == True:
		return render(request,'search/index.html',None)
	else:
		return redirect('/auth')

def query(request,searchWords):
    if request.user.is_authenticated() == True and request.user.is_active == True:
        cur = db.dashboard_project.find({'$text':{'$search':searchWords}},{'password': 0, 'date_joined': 0,'is_staff':0,'fileList':0,'contributorList':0,"search_index_search_list_field":0})
        projects = []
        for c in cur:
            projects.append(c)
        projectJson = dumps(projects)
        cur = db.auth_user.find({'$text':{'$search':searchWords}},{'username':1,'first_name':1,'last_name':1})
        users = []
        for c in cur:
            users.append(c)
        userJson = dumps(users)

        cur = db.event_event.find({'$text':{'$search':searchWords}},{'eventName':1,'description':1,'skillList':1})
        events = []
        for c in cur:
            print c
            events.append(c)
        eventJson = dumps(events)
        data = {'users':userJson,'projects':projectJson,'events':eventJson}
        return HttpResponse(json.dumps(data))
    else:
        return redirect('/auth')

def fromDash(request):
	if request.user.is_authenticated() == True and request.user.is_active == True:
		searchWord = request.GET['search']
		return render(request,'search/index.html',{'searchWord':searchWord})
	else:
		return redirect('/auth')
			
# def query_user(request,searchWords):
# 	if request.user.is_authenticated() == True and request.user.is_active == True:
# 		cur = db.auth_user.find({'$text':{'$search':searchWords}},{'username':1,'first_name':1,'last_name':1})
# 		users = []
# 		for c in cur:
# 			users.append(c)
# 		userJson = dumps(users)
# 		data = {'users':userJson}
# 		return HttpResponse(json.dumps(data))
# 	else:
# 		return redirect('/auth')