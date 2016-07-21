from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login
from django.http import HttpResponse
from postbar.models import TKhomepage

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
				return HttpResponse("登录成功")
		else:
			dic['show1'] = 'inline'
	return render(request, 'postbar/index.html', dic)

def register(request):
	dic = {'show1': 'none', 'show2': 'none', 'show3': 'none', 'show4': 'none', 'show5': 'none'}
	if request.POST:
		name = request.POST['username']
		password = request.POST['password']
		repassword = request.POST['repassword']
		nickname = request.POST['nickname']
		email = request.POST['email']
		q = User.objects.filter(username = name)
		if q or name == '':
			dic['show1'] = 'inline'
		else:
			if password == '':
				dic['show2'] = 'inline'
				return render(request, 'postbar/register.html', dic)
			if password != repassword:
				dic['show3'] = 'inline'
				return render(request, 'postbar/register.html', dic)
			if nickname == '':
				dic['show4'] = 'inline'
				return render(request, 'postbar/register.html', dic)
			if email == '':
				dic['show5'] = 'inline'
				return render(request, 'postbar/register.html', dic)
			TKhomepage.newUser(name, password, email, nickname)
	return render(request, 'postbar/register.html', dic)
