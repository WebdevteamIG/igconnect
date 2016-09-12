

# Create your views here.
from django.shortcuts import render,redirect
from django.http import HttpResponse
from django.shortcuts import get_object_or_404,render
from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from dashboard.models import Project,Document,Rating
from auth.models import Skill
import json,os
from djangotoolbox.fields import ListField,EmbeddedModelField
from dashboard.forms import DocumentForm
from datetime import datetime
from django.core.paginator import Paginator
from bson.json_util import dumps
from django.core import serializers
from django.db.models import Q
from django.views.decorators.csrf import csrf_exempt, csrf_protect
@csrf_exempt
def index(request,pageNo=None):
	if request.user.is_authenticated() and request.user.is_active == True:
		projectList=Project.objects.order_by('-publishedDate')
		paginator = Paginator(projectList,5)
		
		if request.method == 'POST':
				data = json.loads(request.POST['data'])
				json.dumps(data)
				return categorise(data)
	
		if pageNo is None: 
			projects = paginator.page(1)
			projectList = projects.object_list
			myProjects = list()
			for project in projectList:
				myUser = {
					'first_name':project.user.first_name,
					'last_name':project.user.last_name
				}
				existingRating = Rating.objects.filter(Q(project = project), Q(user = request.user)) 
				
				myProject = {
					'publishedDate':project.publishedDate,
					'id':project.id,
					'user':myUser,
					'projectName':project.projectName,
					'projectDescription':project.projectDescription,
					'skillList':project.skillList,
					'rating':"x"*int(project.avgRating),
					'rating2':repr(round(project.avgRating,2)),
					'ratingCount':repr(project.ratingCount),
					
				}
			
				myProjects.append(myProject)
			users=User.objects.all()
			return render(request,'dashboard/projects.html',{'projects':myProjects,'username':request.user.username,'users':users})
		else:
			#pageNo = json.loads(pageNo['branchList'])
			projects = paginator.page(pageNo)
			projectList = projects.object_list
			myProjects = list()
			for project in projectList:
				myUser = {
					'first_name':project.user.first_name,
					'last_name':project.user.last_name
                    
                    
				}
				skills = []
				for skill in project.skillList:
					skills.append(skill.skillName)
				myProject = {
					'id':project.id,
					'user':myUser,
					'projectName':project.projectName,
					'projectDescription':project.projectDescription,
					'skillList':skills,
					'publishedDate':project.publishedDate,
					'rating':"x"*int(project.avgRating+1),
					'rating2':repr(round(project.avgRating,2)),
					'ratingCount':repr(project.ratingCount)
				}
				myProjects.append(myProject)
			return HttpResponse(json.dumps(myProjects),mimetype="application/json")
	else:
		return redirect("/auth/")

def categorise(data):
    projectList = set()
    branch = [int(x) for x in data['branchList']]
    projects = Project.objects.raw_query({'branchList':{'$in':branch}})
    paginator = Paginator(projects,10)
    projectList = paginator.page(data['pageNo'])
    projectList = projectList.object_list
    myProjects = []
    for project in projectList:
        myUser = {
            'first_name':project.user.first_name,
            'last_name':project.user.last_name
            }
        skills = []
        for skill in project.skillList:
            skills.append(skill.skillName)
        myProject = {
            'id':project.id,
            'user':myUser,
            'projectName':project.projectName,
            'projectDescription':project.projectDescription,
            'skillList':skills,
            'publishedDate':project.publishedDate,
            'rating':"x"*int(project.avgRating+1),
            'rating2':repr(round(project.avgRating,2)),
            'ratingCount':repr(project.ratingCount)
            }
        myProjects.append(myProject)
	return HttpResponse(json.dumps(myProjects),mimetype="application/json")

@csrf_exempt
def rate(request):
	if not request.user.is_authenticated() or not request.user.is_active == True:
		redirect("/auth/")

	project = Project.objects.get(id = request.POST.get('projectId'))
	rating = round(float(request.POST.get('rating')),2)
	try:
		existingRating = Rating.objects.get(project = project,user=request.user)
		project.avgRating = (project.avgRating * project.ratingCount - existingRating.rating + rating)/project.ratingCount
		project.save()
		existingRating.rating = rating
		existingRating.save()
		return HttpResponse(repr(project.avgRating))
	except Rating.DoesNotExist:
		newRating = Rating(user = request.user, project = project, rating = rating)
		newRating.save()
		project.avgRating = (project.avgRating*project.ratingCount + rating)/(project.ratingCount+1)
		project.ratingCount += 1
		project.save()
		return HttpResponse(repr(project.avgRating))


def addProject(request):
#    print "hello in project"
    if not  request.user.is_authenticated() or not request.user.is_active == True:
        redirect("/auth/")
    if request.method=="POST":
        requestReceived=json.loads(request.POST.get("project"))
        json.dumps(requestReceived)
        projectName=requestReceived['projectName']
        projectDescription=requestReceived['projectDescription']
        skills=requestReceived['skills']
        branches = requestReceived['branches']
#        projectImage = request.FILES['projectImage']
#        shortDesc = requestReceived['shortDesc']
        skillList=[]
        print len(branches)
        for skillId in skills:
            skill=Skill.objects.get(id=skillId)
            skillList.append(skill)

        contributors=requestReceived['contributers']
        contributorList=[]
        for username in contributors:
            user=User.objects.get(username=username)
            contributorList.append(user)

        currentTimeStamp = datetime.strftime(datetime.now(), '%Y-%m-%d %H:%M')
        project=Project(user=request.user,projectName=projectName,publishedDate=currentTimeStamp,projectDescription=projectDescription,skillList=skillList,contributorList=contributorList,branchList=branches)#,shortDesc=shortDesc,projectImage=projectImage)
        project.save()
        return HttpResponse()


    else:

        users=User.objects.all();
        skills=Skill.objects.all();
        if request.user.is_authenticated():
            return render(request,'dashboard/addprojects.html',{'skills':skills,'users':users,'username':request.user.username})	
        else:
            return redirect("/auth/")

def updateProject(request):
	if request.method=='POST':
		if request.user.is_authenticated() and request.user.is_active == True:
			projectId=request.POST.get('projectId')
			project=Project.objects.get(id=projectId)
			if 'projectName' in request.POST:
				project.projectName=request.POST.get('projectName')
				project.save()
			if 'projectDescription' in request.POST:
				project.projectDescription=request.POST.get('projectDescription')
				project.save()

			if 'skillList' in request.POST:
				skills=json.loads(request.POST.get('skillList'))
				skills=skills['skill']
				#print skills
				#skills=json.loads(skills)
				#print skills
				skillList=[]
				for skillId in skills:
					#print skillId
					skill=Skill.objects.get(id=skillId)
					skillList.append(skill)
				project.skillList=skillList
				print skillList
				project.save()

			if 'contributorList' in request.POST:
				contributors=json.loads(request.POST.get('contributorList'))
				print contributors
				contributors=contributors['contributors']
				contributorList=[]
				print contributors
				for username in contributors:
					print username
					user=User.objects.get(username=username)
					contributorList.append(user)
					project.contributorList=contributorList
					project.save()
			return HttpResponse('success')
		else:
			return HttpResponse('unauthorized')



def viewProject(request):
    if not request.user.is_authenticated() or not request.user.is_active == True:
        return redirect("/auth/")
    if request.method=='GET':
        uploadToken=''
        data={}
        if 'uploadToken' in request.GET and 'uploadToken' in request.session:
            uploadToken=request.GET.get('uploadToken')
            data['uploadToken']=True

        projectId=request.GET.get('projectId')
        project=Project.objects.get(id=projectId)
        data['projectId'] = project.id
        data['projectImage'] = project.projectImage
        data['projectName'] = project.projectName
        data['shortDesc'] = project.shortDesc
        data['projectDescription'] = project.projectDescription
        data['skillList'] = project.skillList
        data['contributorList'] = project.contributorList
        data['projectUsername'] = project.user.username
        data['isOwner'] = (request.user.username == project.user.username)
        #print data['isOwner']
        #print data
        if 'uploadToken' not in request.session and 'alerted' not in request.session:
            request.session['alerted']=True
            return redirect('/dashboard/viewProject/?projectId='+projectId)
        if 'uploadToken' in request.session:
            del request.session['uploadToken']

        allSkills=Skill.objects.all()
        addSkills=[]
        for skill in allSkills:
            flag=False
            for skill2 in project.skillList:
                if skill.id == skill2.id:
                    temp={
                        'belongs':1,
                        'skill':skill
                    }
                    addSkills.append(temp)
                #	print temp
                    flag=True
                    break
            if not flag:
                temp={
                    'belongs':0,
                    'skill':skill
                }
                #print temp
                addSkills.append(temp)
        data['addSkills']=addSkills



        allContributors=User.objects.all()
        addContributors=[]
        for contributor in allContributors:
            flag=False
            for contributor2 in project.contributorList:
                if contributor.id == contributor2.id:
                    temp={
                        'belongs':1,
                        'user':contributor
                    }
                    addContributors.append(temp)
                #	print temp
                    flag=True
                    break
            if not flag:
                temp={
                    'belongs':0,
                    'user':contributor
                }
                #print temp
                addContributors.append(temp)
        data['addContributors']=addContributors
        data['fileList'] = project.fileList
        return render(request,'dashboard/viewproject.html',data)

def deleteDocument(request):
	if not request.user.is_authenticated() or not request.user.is_active == True:
		return redirect("/auth/")
	if request.method=='POST':
		projectId=request.POST['projectId']
		project=Project.objects.get(id=projectId)
		if not (request.user.username == project.user.username) : 
			return HttpResponse('no')
		documentPath=request.POST['documentPath']
		project=Project.objects.get(id=projectId)
		flag=False
		c=0
		print documentPath
		for files in project.fileList:
			if files.document.path == documentPath :
				print files.document.path
				del project.fileList[c]
				flag=True
				break
			c=c+1
		if flag:
			project.save()
			os.remove(documentPath)
			return HttpResponse('success')
		else:
			project.save()
			return HttpResponse('no')



def uploadFiles(request):
	if not request.user.is_authenticated() or not request.user.is_active == True:
		return redirect("/auth/")
	
	if request.method == 'POST':
		#form = DocumentForm(request.POST, request.FILES)
		#print request.POST
		projectId=request.POST.get('projectId')
		#print projectId
		#print request.FILES
		uploadedFiles=request.FILES.getlist('uploadedFile')
		documentName=request.POST.get('documentName')
		project=Project.objects.get(id=projectId)
		for uploadedFile in uploadedFiles :
			print "1"
			project.fileList.append(Document(document=uploadedFile,documentName=documentName))
		project.save()
		request.session['uploadToken'] = True
		if 'alerted' in request.session:
			del request.session['alerted']
		return redirect('/dashboard/viewProject/?projectId='+projectId+"&uploadToken=true")
		return HttpResponse()
	else:
		return render(request,'dashboard/uploadfiles.html',None)