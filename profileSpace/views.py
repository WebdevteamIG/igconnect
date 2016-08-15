from django.shortcuts import render,redirect
from auth.models import UserProfile,Skill
from django.shortcuts import render
from django.http import HttpResponse
from django.contrib.auth.models import User
from dashboard.models import Project
import json,requests
from . import mappings
# Create your views here.

def checkProfilePic(registrationNumber):
	return False
	url = "https://wsdc.nitw.ac.in/student/assets/upload/thumbs/" + registrationNumber + ".jpg"
	r = requests.head(url)
	return r.status_code == 200
	
def index(request,username):
	if request.user.is_authenticated() == True and request.user.is_active == True:
		if username is None:
			userprofile = request.user.get_profile()
			projects = Project.objects.filter(user=userprofile.user)
			contributor = Project.objects.raw_query({'contributorList.username':userprofile.user.username})
			projects = list(projects) + list(contributor)
			userprofile.branch = mappings.branches[int(userprofile.branch)-1]
			userprofile.level = mappings.levels[int(userprofile.level)-1]
			profilePic = checkProfilePic(userprofile.regNum)
			return render(request,'profile/profile.html',{'sendMessage':False,'userData':userprofile,'projects':projects,'profilePic':profilePic})
		else:
			try:
				userprofile = User.objects.get(username=username).get_profile()
				projects = Project.objects.filter(user=userprofile.user)
				contributor = Project.objects.raw_query({'contributorList.username':userprofile.user.username})
				projects = list(projects) + list(contributor)
				userprofile.branch = mappings.branches[int(userprofile.branch)-1]
				userprofile.level = mappings.levels[int(userprofile.level)-1]
				profilePic = checkProfilePic(userprofile.regNum)
		#		return render(request,'profile/profile.html',{'userData':userprofile,'projects':projects,'profilePic':profilePic})

				sendMessage = True
				if userprofile.user == request.user:
					sendMessage = False
				return render(request,'profile/profile.html',{'profilePic':profilePic,'sendMessage':sendMessage,'userData':userprofile,'projects':projects,'from':request.user.username,'to':userprofile.user.username})
			except User.DoesNotExist:
				return render(request,'base/error.html',None)
	else:
		return redirect('/auth/signin')

def complete(request):
	if request.user.is_authenticated() == True and request.user.is_active == True:
		return render(request,'profile/completeProfile.html',None)
	else:
		return redirect('/auth/signin')

def edit(request):
	if request.user.is_authenticated() == True and request.user.is_active == True:
		if request.method == 'POST':	
			first_name = request.POST['first_name']
			last_name = request.POST['last_name']
			email = request.POST['email']
			user = User.objects.get(username=request.user.username)
			
			user.first_name = first_name
			user.last_name = last_name
			user.email = email
			user.save()

			userprofile = UserProfile.objects.get(user=user)

			skills=json.loads(request.POST['skills'])
			userprofile.conferenceList = json.loads(request.POST['conferences'])
			userprofile.MOOCList = json.loads(request.POST['MOOCs'])
			userprofile.researchPaperList = json.loads(request.POST['researchPapers'])
			userprofile.aboutMe = request.POST['aboutMe']
			userprofile.phoneNo = request.POST['phoneNum']
			userprofile.shareNo = request.POST['share']
			userprofile.regNum = request.POST['regNum']
			userprofile.level = request.POST['level']
			userprofile.branch = request.POST['branch']
			skillList = []
			for skill in skills:
				s = Skill.objects.get(id=skill)
				if s is not None:
					skillList.append(s)

			userprofile.skillList = skillList
			#profile = UserProfile(user=request.user,regNum=regNum,branch=branch,level=level,skillList=skillList,
			#	phoneNo=phoneNum,MOOCList=MOOCs,shareNo=shareNo,aboutMe=aboutme,researchPaperList=researchPapers,conferenceList=conferences)
			userprofile.save()
			userprofile.save()
			return HttpResponse("Done")
		else:
			userprofile = request.user.get_profile()
			skills = Skill.objects.all()
			#print userprofile.branch
			return render(request,'profile/edit.html',{'userData':userprofile,'skillList':skills})
	else:
		return render(request,'base/error.html',None)

