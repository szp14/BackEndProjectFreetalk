from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponse, HttpResponseRedirect
from postbar.models import TKhomepage, TKuser, TKpost, TKresponse

@csrf_exempt
def index(request):
	logout(request)
	dic = {'show1': 'none', 'show2': 'none'}
	if request.POST:
		name = request.POST['name1']
		password = request.POST['word1']
		q = User.objects.filter(username = name)
		if q:
			user = authenticate(username = name, password = password)
			if user == None:
				dic['show2'] = 'inline'
			else:
				login(request, user)
				return HttpResponseRedirect('../account/')
		else:
			dic['show1'] = 'inline'
	return render(request, 'postbar/index.html', dic)

def register(request):
	dic = {'show1': 'none', 'show2': 'none', 'show3': 'none', 'show4': 'none', 'show5': 'none', 'show6': 'none', 'show7': 'none'}
	if request.POST:
		name = request.POST['username']
		password = request.POST['password']
		repassword = request.POST['repassword']
		nickname = request.POST['nickname']
		email = request.POST['email']
		question = request.POST['question']
		answer = request.POST['answer']
		tip = False
		q = User.objects.filter(username = name)
		if q or name == '':
			dic['show1'] = 'inline'
		else:
			if password == '':
				dic['show2'] = 'inline'
				tip = True
			if password != repassword:
				dic['show3'] = 'inline'
				tip = True
			if nickname == '':
				dic['show4'] = 'inline'
				tip = True
			if email == '':
				dic['show5'] = 'inline'
				tip = True
			if question == '':
				dic['show6'] = 'inline'
				tip = True
			if answer == '':
				dic['show7'] = 'inline'
				tip = True
			if tip == False:
				TKhomepage.newUser(name, password, email, nickname, question, answer)
				return HttpResponseRedirect('../account/')
	return render(request, 'postbar/register.html', dic)

PREUSER = ""
def findback(request):
	global PREUSER
	dic = {'show1': 'none', 'show2': 'none', 'show3': 'none', 'show4': 'none', 'content1':'', 'content2':'密保问题'}
	if PREUSER != '':
		dic['content1'] = PREUSER.username
		dic['content2'] = PREUSER.tkuser.pwdQuestion
	if request.GET:
		name = request.GET['username']
		q = User.objects.filter(username = name)
		if q:
			PREUSER = q[0]
			dic['content1'] = PREUSER.username
			dic['content2'] = PREUSER.tkuser.pwdQuestion
		else:
			PREUSER = ''
			dic['show1'] = 'inline'
	if request.POST:
		if PREUSER == '':
			dic['show1'] = 'inline'
			return render(request, 'postbar/findback.html', dic)
		success = True
		answer = request.POST['answer']
		password = request.POST['password']
		repassword = request.POST['repassword']
		if answer != PREUSER.tkuser.pwdAnswer:
			dic['show2'] = 'inline'
			success = False
		if password == '':
			dic['show3'] = 'inline'
			success = False
		if repassword != password:
			dic['show4'] = 'inline'
			success = False
		if success:
			PREUSER.tkuser.modifyPwd(password)
			return HttpResponseRedirect('../log/')
	return render(request, 'postbar/findback.html', dic)

def account(request):
	if request.user.is_authenticated():
		return render(request, 'postbar/account.html', {'non':'none'})
	else:
		return HttpResponse("需要登录，请您进行登录操作！")