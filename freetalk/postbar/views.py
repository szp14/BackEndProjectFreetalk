from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponse, HttpResponseRedirect
from postbar.models import TKhomepage, TKuser, TKpost, TKresponse
import json
from django.core.urlresolvers import reverse

@csrf_exempt
def index(request):
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
				return HttpResponseRedirect(reverse('homepage'))
		else:
			dic['show1'] = 'inline'
	return render(request, 'postbar/index.html', dic)

@csrf_exempt
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
				return HttpResponseRedirect(reverse('index'))
	return render(request, 'postbar/register.html', dic)

PREUSER = ""
@csrf_exempt
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
			return HttpResponseRedirect(reverse('index'))
	return render(request, 'postbar/findback.html', dic)
@csrf_exempt
def account(request):
	if request.user.is_authenticated():
		dic = {'username': request.user.username, 'name': request.user.tkuser.nickname, 'email': request.user.email, 
			'question': request.user.tkuser.pwdQuestion, 'img': '/static/images/mengbi.jpg',
			'show1': 'none', 'show2': 'none', 'show3': 'none', 'show4': 'none', 'show5': 'none'
		}
		if request.user.tkuser.img:
			dic['img'] = request.user.tkuser.img.url 
		if request.POST:
			pic = request.FILES.get('headimg')
			name = request.POST['nickname']
			email = request.POST['email']
			answer = request.POST['answer']
			newques = request.POST['newquestion']
			newans = request.POST['newanswer']
			success = 0
			if pic:
				request.user.tkuser.modifyImg(pic)
			if name == '':
				dic['show1'] = 'inline'
				success = -1
			if email == '':
				success = -1
				dic['show5'] = 'inline'
			if answer != '':
				if answer != request.user.tkuser.pwdAnswer:
					dic['show2'] = 'inline'
					success = -1
				if newques == '':
					dic['show3'] = 'inline'
					success = -1
				if newans == '':
					success = -1
					dic['show4'] = 'inline'
				if success != -1:
					success = 1
			if success == 0:
				request.user.tkuser.modifyNickname(name)
				request.user.email = email
				request.user.save()
				return HttpResponseRedirect(reverse('homepage'))
			elif success == 1:
				request.user.tkuser.modifyNickname(name)
				request.user.email = email
				request.user.tkuser.pwdQuestion = newques
				request.user.tkuser.pwdAnswer = newans
				request.user.save()
				request.user.tkuser.save()
				return HttpResponseRedirect(reverse('homepage'))
		return render(request, 'postbar/account.html', dic)
	else:
		return HttpResponse("需要登录，请您进行登录操作！")

@csrf_exempt
def admin(request):
	if request.user.is_authenticated() and request.user.tkuser.usrType != 0:
		if request.POST:
			list1 = request.POST["op"].split()
			user = TKhomepage.searchUsrByName(list1[1])
			dic = {"res": "成功！"}
			if list1[0] == 'silence':
				if user.tkuser.usrStatus == 0:
					user.tkuser.modifyStatus(1)
					dic['res'] = '该用户已被禁言成功！'
				elif user.tkuser.usrStatus == 1:
					user.tkuser.modifyStatus(0)
					dic['res'] = '该用户已被解除禁言！'
				else:
					dic['res'] = '该用户处于屏蔽阶段，无法解除禁言！'
			elif list1[0] == 'hide':
				if user.tkuser.usrStatus == 2:
					user.tkuser.modifyStatus(1)
					dic['res'] = '该用户已被解除屏蔽，但仍处于禁言阶段！'
				else:
					user.tkuser.modifyStatus(2)
					dic['res'] = '该用户已被成功屏蔽！'
			elif list1[0] == 'del':
				TKhomepage.deleteUser(list1[1])
				dic['res'] = '该用户已被成功删除！'
			elif list1[0] == 'change':
				if user.tkuser.usrType == 0:
					dic['res'] = '该用户已成为管理员！'
				else:
					dic['res'] = '该用户已成为普通用户！'
				user.tkuser.modifyPermission(1 - user.tkuser.usrType)
			return HttpResponse(json.dumps(dic))
		users = User.objects.all()
		dic = {'users': users, "type": request.user.tkuser.usrType}
		return render(request, 'postbar/admin.html', dic)
	else:
		return HttpResponse("您未登陆或者没有权限访问该网页！")
	

@csrf_exempt
def homepage(request):
	if request.user.is_authenticated():
		dic = {
			'user': request.user,
			'img' : '/static/images/mengbi.jpg',
		}
		if request.user.tkuser.img:
			dic['img'] = request.user.tkuser.img.url
		if request.POST:
			if 'logout' in request.POST:
				logout(request)
				return HttpResponse(json.dumps({
					'res': '注销登录成功，即将跳转到登录界面！'
				}))
			elif 'title' in request.POST:
				return render(request, 'postbar/homepage.html', dic)
		return render(request, 'postbar/homepage.html', dic)
	else:
		return HttpResponse("您未登陆，无法访问该网页！")
