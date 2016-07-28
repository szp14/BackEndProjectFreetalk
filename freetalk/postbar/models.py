from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
import os
from freetalk.settings import STATIC_ROOT, MEDIA_ROOT
# Create your models here.
# type        0: normal user|1: admin |2: superadmin
# status      0: normal     |1: forbid|2: hidden
# resptype    0: normal     |1: the resp of resp
# upvoteType  0: upvote post|1: upvote resp
def user_directory_path(instance, filename):
	if os.path.isfile(MEDIA_ROOT + '/upload/' + str(instance.user.id)) == True:
		os.remove(MEDIA_ROOT + '/upload/' + str(instance.user.id))
	return 'upload/' + str(instance.user.id)

def postImgPath(instance, filename):
	return 'upload/0' + str(instance.id)

def respImgPath(instance, filename):
	return 'upload/000' + str(instance.id)



class TKuser(models.Model):
	user        = models.OneToOneField(User, on_delete = models.CASCADE)
	nickname    = models.CharField(max_length = 100)
	img         = models.ImageField(upload_to = user_directory_path, default = '/static/images/mengbi.jpg')
	pwdQuestion = models.CharField(max_length = 100)
	pwdAnswer   = models.CharField(max_length = 100)
	numPost     = models.IntegerField(default = 0)
	numScore    = models.IntegerField(default = 0)
	numCoin     = models.IntegerField(default = 0)
	usrStatus   = models.SmallIntegerField(default = 0)
	usrType     = models.SmallIntegerField(default = 0)

	def getImgUrl(self):
		return self.img.url

	def modifyPwd(self, newPwd):
		self.user.set_password(newPwd)
		self.user.save()

	def modifyNickname(self, newNickname):
		self.nickname = newNickname
		self.save()

	def modifyImg(self, newImg):
		self.img = newImg
		self.save()

	def modifyStatus(self, newStatus):
		self.usrStatus = newStatus
		self.save()

	def modifyPermission(self, newPermission):
		self.usrType = newPermission
		self.save()

	def getPost(self):
		return TKpost.objects.filter(user = self.user)

	def newPost(self, title, content, imgList, attachment, classTag, keyword):
		q = TKpost(title = title, content = content, attachment = attachment, classTag = classTag, keyword = keyword, user = self.user)
		q.save()
		self.numPost = self.numPost + 1
		self.save()
		if imgList != None:
			for img in imgList:
				p = TKpostImage(img = img, post = q)
				p.save()

	def upvotePost(self, postId):
		if TKupvoteRelation.isUpvoted(0, self.id, postId):
			return False
		q = TKpost.objects.filter(id = postId)
		if q:
			q = q[0]
			q.score = q.score + 1
			q.save()
			q.user.tkuser.numScore = q.user.tkuser.numScore + 1
			q.user.tkuser.save()
			TKupvoteRelation.newRelation(0, self.id, postId)
		return True

	def downvotePost(self, postId):
		if TKupvoteRelation.isUpvoted(0, self.id, postId) == False:
			return False
		q = TKpost.objects.filter(id = postId)
		if q:
			q = q[0]
			q.score = q.score - 1
			q.save()
			q.user.tkuser.numScore = q.user.tkuser.numScore - 1
			q.user.tkuser.save()
			TKupvoteRelation.delRelation(0, self.id, postId)
		return True

	def giveCoinPost(self, postId, num):
		q = TKpost.objects.filter(id = postId)
		if q and self.numCoin > num:
			q = q[0]
			q.coin = q.coin + num
			q.save()
			q.user.tkuser.numCoin = q.user.tkuser.numCoin + num
			q.user.tkuser.save()
			self.numCoin = self.numCoin - num
			self.save()
			return True
		else:
			return False

	def highlightPost(self, post, numCoin):
		if self.numCoin < numCoin:
			return False
		self.numCoin = self.numCoin - numCoin
		post.highlight = 1
		post.save()
		self.save()

	def newResp(self, respType, content, imgList, attachment, postId, respId):
		q = None
		p = TKpost.objects.filter(id = postId)
		p = p[0] if p else None
		p.numResp = p.numResp + 1
		p.save()
		r = TKresponse.objects.filter(id = respId)
		hostId = r[0].user.id if r else 0
		q = TKresponse(respType = respType, content = content, attachment = attachment, user = self.user, post = p, respId = respId, hostId = hostId)
		q.save()
		if imgList != None:
			for img in imgList:
				p = TKrespImage(img = img, resp = q)
				p.save()

	def upvoteResp(self, respId):
		if TKupvoteRelation.isUpvoted(1, self.id, respId):
			return False
		q = TKresponse.objects.filter(id = respId)
		if q:
			q = q[0]
			q.score = q.score + 1
			q.save()
			q.user.tkuser.numScore = q.user.tkuser.numScore + 1
			q.user.tkuser.save()
			TKupvoteRelation.newRelation(1, self.id, respId)
		return True

	def downvoteResp(self, respId):
		if TKupvoteRelation.isUpvoted(1, self.id, respId) == False:
			return False
		q = TKresponse.objects.filter(id = respId)
		if q:
			q = q[0]
			q.score = q.score - 1
			q.save()
			q.user.tkuser.numScore = q.user.tkuser.numScore - 1
			q.user.tkuser.save()
			TKupvoteRelation.delRelation(1, self.id, respId)
		return True

class TKpost(models.Model):
	title       = models.CharField(max_length = 100)
	content     = models.CharField(max_length = 1000)
	attachment  = models.FileField(upload_to = 'upload', null = True)
	user        = models.ForeignKey(User, on_delete = models.CASCADE)
	time        = models.DateTimeField(default = timezone.now)
	classTag    = models.CharField(max_length = 100)
	keyword     = models.CharField(max_length = 100)
	numClick    = models.IntegerField(default = 0)
	numResp     = models.IntegerField(default = 0)
	score       = models.IntegerField(default = 0)
	coin        = models.IntegerField(default = 0)
	highlight   = models.SmallIntegerField(default = 0)

	def getImgList(self):
		return TKpostImage.objects.filter(post = self)

	def clicked(self):
		self.numClick = self.numClick + 1
		self.save()

	def isTagExist(self, tagname):
		taglist = self.classTag.split()
		for tag in taglist:
			if tag == tagname:
				return True
		return False

	def addTag(self, tagname):
		if self.isTagExist(tagname) == False:
			self.classTag += ' ' + tagname
			self.save()

	def delTag(self, tagname):
		taglist = self.classTag.split()
		for tag in taglist:
			if tag == tagname:
				taglist.remove(tagname)
		if len(taglist) > 0:
			classTag = taglist[0]
			for tag in taglist[1:len(taglist)]:
				classTag += ' ' + tag
			self.classTag = classTag
			self.save()

	def deletePost(self):
		self.user.tkuser.numPost = self.user.tkuser.numPost - 1
		self.user.tkuser.save()
		self.delete()

	def getTagNum(self):
		taglist = self.classTag.split()
		return len(taglist)

	def getResp(self):
		return TKresponse.objects.filter(post = self, respType = 0)

	def getPostById(postId):
		post = TKpost.objects.filter(id = postId)
		if post:
			return post[0]
		else:
			return None

	def focusOnHost(self):
		return TKresponse.objects.filter(user = self.user, post = self, respType = 0)

class TKresponse(models.Model):
	respType    = models.SmallIntegerField(default = 0)
	content     = models.CharField(max_length = 400)
	user        = models.ForeignKey(User, on_delete = models.CASCADE)
	post        = models.ForeignKey(TKpost, on_delete = models.CASCADE)
	attachment  = models.FileField(upload_to = 'upload', null = True)
	respId      = models.IntegerField()
	hostId      = models.IntegerField()
	time        = models.DateTimeField(default = timezone.now)
	score       = models.IntegerField(default = 0)

	def getImgList(self):
		return TKrespImage.objects.filter(resp = self)

	def getResp(self):
		if self.respType == 0:
			return TKresponse.objects.filter(respId = self.id)

	def getBothSides(self):
		q = User.objects.filter(id = self.hostId)
		return [self.user.tkuser.nickname, q[0].tkuser.nickname] if q else None

	def deleteResp(self):
		q = TKresponse.objects.filter(respId = self.id)
		self.post.numResp = self.post.numResp - 1 - len(q)
		q.delete()
		self.post.save()
		self.delete()

class TKpostImage(models.Model):
	img   = models.ImageField(upload_to = postImgPath)
	post  = models.ForeignKey(TKpost, on_delete = models.CASCADE)

class TKrespImage(models.Model):
	img   = models.ImageField(upload_to = respImgPath)
	resp  = models.ForeignKey(TKresponse, on_delete = models.CASCADE)

class TKclassTag(models.Model):
	classTagName = models.CharField(max_length = 100)

	def deleteClassTag(self):
		basicTag = '清华大学'
		posts = TKhomepage.searchPostByClassTag(self.classTagName)
		for p in posts:
			if p.getTagNum() == 1:
				p.classTag = basicTag
			else:
				p.classTag = ' '.join([tag for tag in p.classTag.split() if tag != self.classTagName])
			p.save()
		self.delete()

	def modifyClassTag(self, newTag):
		newTag = newTag.strip()
		if TKclassTag.objects.filter(classTagName = newTag):
			return False
		posts = TKhomepage.searchPostByClassTag(self.classTagName)
		for p in posts:
			p.classTag = ' '.join([tag for tag in p.classTag.split() if tag != self.classTagName])
			p.classTag = p.classTag + (newTag if p.classTag == '' else ' ' + newTag)
			p.save()
		self.classTagName = newTag
		self.save()
		return True

	def getPostNum(self):
		return len(TKhomepage.searchPostByClassTag(self.classTagName))

	def getRespNum(self):
		respNum = 0
		posts = TKhomepage.searchPostByClassTag(self.classTagName)
		for post in posts:
			respNum = respNum + post.numResp
		return respNum

	def getClickNum(self):
		click = 0
		posts = TKhomepage.searchPostByClassTag(self.classTagName)
		for post in posts:
			click = click + post.numClick
		return click

	def getScoreNum(self):
		scores = 0
		posts = TKhomepage.searchPostByClassTag(self.classTagName)
		for post in posts:
			scores = scores + post.score
		return scores

	def getCoinNum(self):
		coins = 0
		posts = TKhomepage.searchPostByClassTag(self.classTagName)
		for post in posts:
			coins = coins + post.coin
		return coins

class TKupvoteRelation(models.Model):
	upvoteType = models.SmallIntegerField(default = 0)
	user       = models.ForeignKey(User, on_delete = models.CASCADE)
	post       = models.ForeignKey(TKpost, on_delete = models.CASCADE, null = True)
	resp       = models.ForeignKey(TKresponse, on_delete = models.CASCADE, null = True)

	def newRelation(upvoteType, userId, upId):
		p = TKhomepage.searchUsrById(userId)
		r = None
		if upvoteType == 0:
			r = TKpost.objects.filter(id = upId)
		else:
			r = TKresponse.objects.filter(id = upId)
		r = r[0] if r else None
		if upvoteType == 0:
			q = TKupvoteRelation(upvoteType = upvoteType, user = p, post = r)
		else:
			q = TKupvoteRelation(upvoteType = upvoteType, user = p, resp = r)
		q.save()

	def isUpvoted(upvoteType, userId, upId):
		p = TKhomepage.searchUsrById(userId)
		r = None
		if upvoteType == 0:
			r = TKpost.objects.filter(id = upId)
		else:
			r = TKresponse.objects.filter(id = upId)
		r = r[0] if r else None
		if upvoteType == 0:
			q = TKupvoteRelation.objects.filter(upvoteType = upvoteType, user = p, post = r)
		else:
			q = TKupvoteRelation.objects.filter(upvoteType = upvoteType, user = p, resp = r)
		return True if q else False

	def delRelation(upvoteType, userId, upId):
		p = TKhomepage.searchUsrById(userId)
		r = None
		if upvoteType == 0:
			r = TKpost.objects.filter(id = upId)
		else:
			r = TKresponse.objects.filter(id = upId)
		r = r[0] if r else None
		if upvoteType == 0:
			q = TKupvoteRelation.objects.filter(upvoteType = upvoteType, user = p, post = r)
		else:
			q = TKupvoteRelation.objects.filter(upvoteType = upvoteType, user = p, resp = r)
		if q:
			q.delete()

class TKhomepage:
	def newAdmin():
		if User.objects.filter(username = 'admin'):
			return
		q = User.objects.create_user('admin', '', 'abcdefgh')
		q.is_staff = True
		q.is_superuser = True
		q.save()
		u = TKuser(nickname = 'admin', pwdQuestion = 'Are you admin?', pwdAnswer = 'Maybe', user = q, numCoin = 100000)
		u.usrType = 2
		u.save()
		TKhomepage.addClassTag('清华大学')
		TKhomepage.addClassTag('教务教学')
		TKhomepage.addClassTag('宿舍风采')
		TKhomepage.addClassTag('实习经验')
		TKhomepage.addClassTag('社团活动')
		TKhomepage.addClassTag('社会实践')
		TKhomepage.addClassTag('科学研究')

	def newUser(username, password, email, nickname, pwdQuestion, pwdAnswer):
		q = User.objects.create_user(username, email, password)
		q.save()
		u = TKuser(nickname = nickname, pwdQuestion = pwdQuestion, pwdAnswer = pwdAnswer, user = q)
		u.save()

	def deleteUser(username):
		q = User.objects.filter(username = username)
		if q:
			q = q[0]
			if os.path.isfile(MEDIA_ROOT + '/upload/' + str(q.id)) == True:
				os.remove(MEDIA_ROOT + '/upload/' + str(q.id))
			q.delete()

	def addClassTag(newClassTag):
		newClassTag = newClassTag.strip()
		if(TKclassTag.objects.filter(classTagName = newClassTag)):
			return False
		q = TKclassTag(classTagName = newClassTag)
		q.save()
		return True


	def searchUsrByNickname(nickname):
		q = tkuser.objects.filter(nickname = nickname)
		return [p.user for p in q]

	def searchUsrById(usrId):
		q = User.objects.filter(id = usrId)
		if q:
			return q[0]
		else:
			return None
	
	def searchUsrByName(name):
		q = User.objects.filter(username = name)
		if q:
			return q[0]
		else:
			return None

	def searchPostByUsrId(usrId):
		return TKpost.objects.filter(user = User.objects.filter(id = usrId)[0])

	def searchPostByKeyword(keyword):
		return TKpost.objects.filter(keyword__contains = keyword)

	def searchPostByClassTag(classTag):
		return TKpost.objects.filter(classTag__contains = classTag)

	def sortPostByTime():
		return TKpost.objects.all().order_by('-time')

	def sortPostByScore():
		return TKpost.objects.all().order_by('-score') 

	def sortPostByCoin():
		return TKpost.objects.all().order_by('-coin')

	def sortPostByClick():
		return TKpost.objects.all().order_by('-numClick')

	def sortPostByResp():
		return TKpost.objects.all().order_by('-numResp')

	def searchPostByTitle(title):
		return TKpost.objects.filter(title__contains = title)

	def searchPostByContent(content):
		return TKpost.objects.filter(content__contains = content)

	def searchRespByUsrId(usrId):
		return TKresponse.objects.filter(user = User.objects.filter(id = usrId)[0])

	def searchRespByPostId(postId):
		return TKresponse.objects.filter(post = TKpost.objects.filter(id = postId)[0])
