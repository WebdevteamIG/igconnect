from django.shortcuts import render,redirect
from message.models import Message,Chat
from django.http import HttpResponse
from django.contrib.auth.models import User
from django.db.models import Q
from datetime import datetime


def send(request):
	if not request.user.is_authenticated() or not request.user.is_active :
		return HttpResponse("-1")

	receiver = User.objects.get(username=request.POST.get('to'))
	sender = User.objects.get(username=request.POST.get('from'))
	body = request.POST.get('body')
	i = 0
	current = datetime.strftime(datetime.now(), '%Y-%m-%d %H:%M')
	profile = receiver.get_profile()
	profile.notify = profile.notify + 1
	profile.save()
	chats = Chat.objects.all()
	message = Message(receiver=receiver,sender=sender,body=body,time=current)
	message.save()
	for chat in chats :
		if ( chat.receiver == receiver and chat.sender == sender ) or (chat.receiver == sender and chat.sender == receiver) :
			temp = Chat.objects.get(id=chats[i].id)
			temp.notify = temp.notify + 1
			print temp.notify
			temp.messages.append(message)
			temp.time = current
			temp.save()
			#print i
			return HttpResponse("2");

		else:
			i=i+1

	if i==len(chats):
		print "2"
		messages=[]
		messages.append(message)
		chat=Chat(notify=1,time=current,receiver=receiver,sender=sender,messages=messages)
		chat.save()
		return HttpResponse("1");



def index(request,id=None):
	if not request.user.is_authenticated() or not request.user.is_active :
		return redirect('/auth/signin')
	profile = request.user.get_profile()
	profile.notify = 0
	profile.save()
	if id is None :
		chats = Chat.objects.filter(Q(receiver=request.user) | Q(sender=request.user)).order_by('-time')
		lasts=[]
		for chat in chats:
			#print chat.notify
			lasts.append(chat.messages[-1])
		return render(request,'message/viewall.html',{'chats':zip(chats,lasts),'name':request.user.username})

	else :
		print "in here"
		chat=Chat.objects.get(id=id)
		if chat.messages[-1].receiver == request.user :
			chat.notify=0
			chat.save()
		print request.user.username
		print chat.receiver.username
		print chat.sender.username
		if not chat.receiver == request.user and not chat.sender==request.user:
			return redirect("/auth/signin") 
		to=chat.receiver
		if chat.receiver == request.user :
			to=chat.sender
		return render(request,'message/viewchat.html',{'to':to.username,'from':request.user.username,'chat':chat,'name':request.user.username})