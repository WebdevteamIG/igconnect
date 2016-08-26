from django.http import HttpResponse
from django.shortcuts import get_object_or_404,render,redirect
from django.contrib.auth import authenticate,login
from django.contrib.auth import logout
from django.contrib.auth.models import User
from auth.models import Skill,UserProfile
import json
from django.views.decorators.csrf import csrf_exempt, csrf_protect
# Create your views here.

def index(request):

	if request.user.is_authenticated() and request.user.is_active == True:
		return redirect('/dashboard')
	else:
		return redirect('/auth/signin')



def signout(request):
	#print "logging out" this also clears all session data
	logout(request) 
	return redirect('/auth/')

@csrf_exempt
def signin(request):
	if request.user.is_authenticated() == True and request.user.is_active == True:
		return redirect('/dashboard')
	if request.method == 'POST':
		username = request.POST['username']
		password = request.POST['password']
		user = authenticate(username=username,password=password)
		if user is None:
			return render(request,'auth/signin.html',{'error':'Invalid username or password'})
		elif user.is_active == False:
			login(request,user)
			return redirect('/auth/register')
		else:
			login(request,user)
			return redirect('/dashboard/') #render the dashboard page
	else:
		print "no post"
		return render(request,'auth/signin.html',None)

@csrf_exempt
def signup(request):
	if request.user.is_authenticated() == True and request.user.is_active == True:
		return redirect('/dashboard')
	if request.method == 'POST':
		username = request.POST['username']
		password = request.POST['password']
		password2 = request.POST['password2']
		firstName = request.POST['firstName']
		lastName = request.POST['lastName']
		if password2 != password:
			return render(request,'auth/signup.html',{'error':'Password doesn\'t match'}) 

		emailAddr = request.POST['email']

		try:
			u = User._default_manager.get(username__iexact=username) #fix for case sensitive username
			return render(request,'auth/signup.html',{'error':'username already already exists!'})
		except User.DoesNotExist:
			user = User.objects.create_user(username=username,email=emailAddr,first_name=firstName,last_name=lastName)
			user.set_password(password)
			user.is_active = False #user will be active only when he completes registration
			user.save()
			user.backend = 'django.contrib.auth.backends.ModelBackend' #user backend error fix
			authenticate(username=username,password=password)
			login(request,user)
			#return redirect('/auth/register')
			skills = Skill.objects.all()
			return render(request,'auth/register.html',{'skillList':skills})
	else:
		return render(request,'auth/signup.html',None)

@csrf_exempt
def register(request):
	if request.user.is_active == True:
			return redirect('/dashboard')

	if request.method == 'POST':
		skills=json.loads(request.POST['skills'])
		conferences = json.loads(request.POST['conferences'])
		MOOCs = json.loads(request.POST['MOOCs'])
		researchPapers = json.loads(request.POST['researchPapers'])
		aboutme = request.POST['aboutMe']
		phoneNum = request.POST['phoneNum']
		shareNo = request.POST['share']
		regNum = request.POST['regNum']
		level = request.POST['level']
		branch = request.POST['branch']
		skillList = []
		for skill in skills:
			s = Skill.objects.get(id=skill)
			if s is not None:
				skillList.append(s)

		profile = UserProfile(user=request.user,regNum=regNum,branch=branch,level=level,skillList=skillList,
			phoneNo=phoneNum,MOOCList=MOOCs,shareNo=shareNo,aboutMe=aboutme,researchPaperList=researchPapers,conferenceList=conferences)
		if profile is None:
			return HttpResponse("Error")
		else:
			profile.save()
			request.user.is_active = True
			request.user.save()
			return HttpResponse("Done")
		
	else:
		skills = Skill.objects.all()
		return render(request,'auth/register.html',{'skillList':skills})
