from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponse, HttpResponseRedirect
from postbar.models import TKhomepage, TKuser, TKpost, TKresponse, TKclassTag, TKupvoteRelation, TKpostImage
import json
from django.core.urlresolvers import reverse
from django.utils import timezone
import re

@csrf_exempt
def index(request):
	dic = {'show1': 'none', 'show2': 'none', 'coin': json.dumps('no')}
	if request.POST:
		if 'login' in request.POST:
			return HttpResponse(json.dumps({
					'res': '登录成功'
				}))
		name = request.POST['name1']
		password = request.POST['word1']
		q = User.objects.filter(username = name)
		if q:
			user = authenticate(username = name, password = password)
			if user == None:
				dic['show2'] = 'inline'
			else:
				timeNow = timezone.now()
				if user.last_login == None or timeNow.year != user.last_login.year or timeNow.month != user.last_login.month or timeNow.day != user.last_login.day:
					user.tkuser.numCoin = user.tkuser.numCoin + 2
					user.tkuser.save()
					dic['coin'] = json.dumps("yes")
					login(request, user)
					return render(request, 'postbar/index.html', dic)
				else:
					login(request, user)
					return HttpResponseRedirect(reverse('homepage', args=('time', 1)))
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
			else:
				if '@' in email and '.com' in email:
					isMatch = True
				else:
					isMatch = False
				if isMatch == False:
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
			'question': request.user.tkuser.pwdQuestion, 'img': request.user.tkuser.getImgUrl(),
			'show1': 'none', 'show2': 'none', 'show3': 'none', 'show4': 'none', 'show5': 'none'
		}
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
				return HttpResponseRedirect(reverse('homepage', args=('time', 1)))
			elif success == 1:
				request.user.tkuser.modifyNickname(name)
				request.user.email = email
				request.user.tkuser.pwdQuestion = newques
				request.user.tkuser.pwdAnswer = newans
				request.user.save()
				request.user.tkuser.save()
				return HttpResponseRedirect(reverse('homepage', args=('time', 1)))
		return render(request, 'postbar/account.html', dic)
	else:
		return HttpResponse("需要登录，请您进行登录操作！")

@csrf_exempt
def useradmin(request, page):
	page = int(page)
	pageEveNum = 20
	TotalNum = len(TKuser.objects.all())
	if TotalNum % pageEveNum == 0 and TotalNum != 0:
		pageNum = TotalNum / pageEveNum
	else:
		pageNum = TotalNum // pageEveNum + 1
	if page > pageNum or page < 1:
		return HttpResponse("该页不存在！")
	if request.user.is_authenticated() and request.user.tkuser.usrType != 0:
		userlist = User.objects.all()[pageEveNum * (page - 1) : pageEveNum * page]
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
		dic = {
			'users': userlist, 
			"type": request.user.tkuser.usrType,
			'pagenum': int(pageNum),
			'page': page,
		}
		return render(request, 'postbar/admin.html', dic)
	else:
		return HttpResponse("您未登陆或者没有权限访问该网页！")
	
@csrf_exempt
def homepage(request, type, page):
	if request.user.is_authenticated():
		page = int(page)
		pageEveNum = 20
		if type == 'time':
			allpost = TKhomepage.sortPostByTime()
		elif type == 'click':
			allpost = TKhomepage.sortPostByClick()
		elif type == 'up':
			allpost = TKhomepage.sortPostByScore()
		elif type == 'respond':
			allpost = TKhomepage.sortPostByResp()
		elif type == 'coin':
			allpost = TKhomepage.sortPostByCoin()
		else:
			wordlist = type.split()
			if wordlist[0] != '无':
				allpost = set(TKhomepage.searchPostByClassTag(wordlist[0]))
			else:
				allpost = set(TKhomepage.sortPostByTime())
			if len(wordlist) > 1:
				for word in wordlist[1: len(wordlist)]:
					list1 = set(TKhomepage.searchPostByTitle(word))
					list2 = set(TKhomepage.searchPostByContent(word))
					allpost = (list1 | list2) & allpost
			allpost = list(allpost)
		TotalNum = len(allpost)
		if TotalNum % pageEveNum == 0 and TotalNum != 0:
			pageNum = TotalNum / pageEveNum
		else:
			pageNum = TotalNum // pageEveNum + 1
		if page > pageNum or page < 1:
			return(HttpResponse("该页面不存在！"))
		postlist = allpost[pageEveNum * (page - 1) : pageEveNum * page]
		postDic = [{'post': p, 
					'tag1': p.classTag.split()[0], 
					'tag2': p.classTag.split()[1] if len(p.classTag.split()) > 1 else '无', 
					'tag3': p.classTag.split()[2] if len(p.classTag.split()) > 2 else '无'
				} for p in postlist
			]
		dic = {
			'user': request.user,
			'img' : request.user.tkuser.getImgUrl(),
			'posts': postDic,
			'tags': TKclassTag.objects.all(),
			'pagenum': int(pageNum),
			'page': page,
		}
		if request.POST:
			if 'logout' in request.POST:
				logout(request)
				return HttpResponse(json.dumps({
					'res': '注销登录成功，即将跳转到登录界面！'
				}))
			elif 'addTag' in request.POST:
				add1 = request.POST['addTag']
				del1 = request.POST['delTag']
				postid = request.POST['id']
				post = postlist[int(postid) - 1]
				res = {
					'tip': '帖子的类标数不能大于三，无法继续增加类标！',
					'type': 0
				}
				if add1 != '无' and del1 == '无' and post.getTagNum() >= 3:
					res['tip'] = '帖子的类标数不能大于三，无法继续增加类标！'
					return HttpResponse(json.dumps(res))
				if add1 == '无' and del1 != '无' and post.getTagNum() <= 1:
					res['tip'] = '帖子的类标数不能少于一，无法继续删除类标！'
					return HttpResponse(json.dumps(res))
				if add1 != '无':
					post.addTag(add1)
				if del1 != '无':
					post.delTag(del1)
				res['tip'] = '修改类标成功！'
				res['type'] = 1
				return HttpResponse(json.dumps(res))
			elif 'delPost' in request.POST:
				postid = request.POST['delPost']
				post = postlist[int(postid) - 1]
				post.deletePost()
				res = {
					'tip': '该帖子已被成功删除！',
				}
				return HttpResponse(json.dumps(res))
			elif 'title' in request.POST:
				high = request.POST.getlist("highlight")
				tag1 = request.POST['tag1']
				tag2 = request.POST['tag2']
				tag3 = request.POST['tag3']
				tags = tag1
				if tag2 != '无' and tag2 != tag1:
					tags += " " + tag2
				if tag3 != "无" and tag1 != tag3:
					if tag2 != "无":
						if tag3 != tag2:
							tags += " " + tag3
					else:
						tags += " " + tag3
				img = [request.FILES.get('img')] if request.FILES.get('img') else None
				attachment = request.FILES.get('attachment') if request.FILES.get('attachment') else None
				newpost = request.user.tkuser.newPost(request.POST['title'], request.POST['content'], img, attachment, tags, "")
				if high:
					request.user.tkuser.highlightPost(newpost, 10)
				if type == 'time':
					allpost = TKhomepage.sortPostByTime()
				elif type == 'click':
					allpost = TKhomepage.sortPostByClick()
				elif type == 'up':
					allpost = TKhomepage.sortPostByScore()
				elif type == 'respond':
					allpost = TKhomepage.sortPostByResp()
				else:
					allpost = TKhomepage.sortPostByCoin()
				postlist = allpost[pageEveNum * (page - 1) : pageEveNum * page]
				dic["posts"] = [{'post': p, 
						'tag1': p.classTag.split()[0], 
						'tag2': p.classTag.split()[1] if len(p.classTag.split()) > 1 else '无', 
						'tag3': p.classTag.split()[2] if len(p.classTag.split()) > 2 else '无'
					} for p in postlist
				]
				return HttpResponseRedirect(reverse('homepage', args=('time', 1)))
			elif 'postid' in request.POST:
				postid = int(request.POST['postid'])
				postlist[postid - 1].clicked()
				return HttpResponse(json.dumps({
					'res': '点击成功'
				}))
		return render(request, 'postbar/homepage.html', dic)
	else:
		return HttpResponse("您未登陆，无法访问该网页！")

@csrf_exempt
def showpost(request, postid, page):
	post = TKpost.getPostById(postid)
	page = int(page)
	pageEveNum = 20
	TotalNum = len(post.getResp())
	if TotalNum % pageEveNum == 0 and TotalNum != 0:
		pageNum = TotalNum / pageEveNum
	else:
		pageNum = TotalNum // pageEveNum + 1
	if page > pageNum or page < 1:
		return HttpResponse("该页不存在！")
	if post and request.user.is_authenticated():
		allrepost = post.getResp()
		repostlist = allrepost[pageEveNum * (page - 1) : pageEveNum * page]
		respDic = [{'resp': p, 
			'respList': p.getResp(), 
			'upvote': '取消点赞' if TKupvoteRelation.isUpvoted(1, request.user.id, p.id) else '点 赞', 
			'num': pageEveNum * (page - 1) + i + 1,
			'imglist': p.getImgList(),
		} for i, p in enumerate(repostlist)]
		dic = {
			'img': post.user.tkuser.getImgUrl(),
			'post': post,
			'imglist': post.getImgList(),
			'reposts': respDic,
			'user': request.user,
			'pagenum': int(pageNum),
			'page': page,
			'host': "只看楼主",
			'upvote': '取消点赞' if TKupvoteRelation.isUpvoted(0, request.user.id, post.id) else '点 赞'
		}
		if request.POST:
			if 'content' in request.POST:
				img = [request.FILES.get('img')] if request.FILES.get('img') else None
				attachment = request.FILES.get('attachment') if request.FILES.get('attachment') else None
				request.user.tkuser.newResp(0, request.POST['content'], img, attachment, post.id, -1)
				return HttpResponseRedirect(reverse('post', args=(postid, 1)))
			if 'setonly' in request.POST:
				if request.POST['setonly'] == "只看楼主":
					repostlist = [r for r in repostlist if r.user == post.user]
					dic['reposts'] = respDic = [{'resp': p, 
						'respList': p.getResp(), 
						'upvote': '取消点赞' if TKupvoteRelation.isUpvoted(1, request.user.id, p.id) else '点 赞', 
						'num': pageEveNum * (page - 1) + i + 1,
						'imglist': p.getImgList(),
					} for i, p in enumerate(repostlist)]
					dic['host'] = "取消只看楼主"
				else:
					dic['reposts'] = respDic = [{'resp': p, 
						'respList': p.getResp(), 
						'upvote': '取消点赞' if TKupvoteRelation.isUpvoted(1, request.user.id, p.id) else '点 赞', 
						'num': pageEveNum * (page - 1) + i + 1,
						'imglist': p.getImgList(),
					} for i, p in enumerate(repostlist)]
					dic['host'] = "只看楼主"
				return render(request, 'postbar/post.html', dic)
			if 'recon' in request.POST:
				if len(repostlist[int(request.POST['id']) - 1].getResp()) > 9:
					return HttpResponse(json.dumps({
						'res': '该帖子的回复数已经大于等于10，您无法继续回复该帖！'
					}))
				request.user.tkuser.newResp(1, request.POST["recon"], None, None, post.id, repostlist[int(request.POST['id']) - 1].id)
				return HttpResponse(json.dumps({
					'res': '回复成功！'
				}))
			if 'reid' in request.POST:
				repostlist[int(request.POST['reid']) - 1].getResp()[int(request.POST['rereid']) - 1].deleteResp()
				return HttpResponse(json.dumps({
					'res': '成功删除该回复！'
				}))
			if 'delreid' in request.POST:
				repostlist[int(request.POST['delreid']) - 1].deleteResp()
				return HttpResponse(json.dumps({
					'res': '成功删除该回复！'
				}))
			if 'vote' in request.POST:
				suc = request.user.tkuser.upvotePost(post.id)
				if suc:
					return HttpResponse(json.dumps({
						'res': '点赞成功！'
					}))
				else:
					request.user.tkuser.downvotePost(post.id)
					return HttpResponse(json.dumps({
						'res': '取消点赞成功！'
					}))
			if 'upvote' in request.POST:
				suc = request.user.tkuser.upvoteResp(repostlist[int(request.POST["upvote"]) - 1].id)
				if suc:
					return HttpResponse(json.dumps({
						'res': '点赞成功！'
					}))
				else:
					request.user.tkuser.downvoteResp(repostlist[int(request.POST["upvote"]) - 1].id)
					return HttpResponse(json.dumps({
						'res': '取消点赞成功！'
					}))
			if 'coin' in request.POST:
				coin = int(request.POST['coin'])
				if coin < 1 or coin > request.user.tkuser.numCoin:
					return HttpResponse(json.dumps({
						'res': '金币数不为正数或者超过了用户拥有的金币数！'
					}))
				else:
					request.user.tkuser.giveCoinPost(post.id, coin)
					return HttpResponse(json.dumps({
						'res': '赠送金币成功！'
					}))
		return render(request, 'postbar/post.html', dic)
	else:
		return HttpResponse("您未登陆或该帖子不存在(可能已经被删除)！")

@csrf_exempt
def tagadmin(request, page):
	page = int(page)
	pageEveNum = 20
	TotalNum = len(TKclassTag.objects.all())
	if TotalNum % pageEveNum == 0 and TotalNum != 0:
		pageNum = TotalNum / pageEveNum
	else:
		pageNum = TotalNum // pageEveNum + 1
	if page > pageNum or page < 1:
		return HttpResponse("该页不存在！")
	if request.user.is_authenticated() and request.user.tkuser.usrType != 0:
		alltag = TKclassTag.objects.all()
		taglist = alltag[pageEveNum * (page - 1) : pageEveNum * page]
		tagInfo = [{'name': p.classTagName, 'post': p.getPostNum(), 'resp': p.getRespNum(), 'click': p.getClickNum(), 'score': p.getScoreNum(), 'coin': p.getCoinNum()} for p in taglist]
		dic = {
			'tags': tagInfo,
			'pagenum': int(pageNum),
			'page': page,
		}
		if 'tag' in request.POST:
			suc = TKhomepage.addClassTag(request.POST['tag'])
			if suc == True:
				data = {
					'res': '增加类标成功！'
				}
			else:
				data = {
					'res': '已经存在一个同名的类标，无法增加！'
				}
			return HttpResponse(json.dumps(data))
		if 'deltag' in request.POST:
			taglist[int(request.POST['deltag']) - 1].deleteClassTag()
			return HttpResponse(json.dumps({
					'res': '删除类标成功！'
				}))
		if 'chatag' in request.POST:
			suc = taglist[int(request.POST['chatag']) - 1].modifyClassTag(request.POST['tagname'])
			if suc == True:
				data = {
					'res': '修改类标成功！'
				}
			else:
				data = {
					'res': '已经存在一个同名的类标，无法修改！'
				}
			return HttpResponse(json.dumps(data))
		return render(request, 'postbar/label.html', dic)
	else:
		return HttpResponse("您未登陆或者没有权限访问该网站！")