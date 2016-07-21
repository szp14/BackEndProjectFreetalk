from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
# Create your models here.
# type     0: normal user|1: admin |2: superadmin
# status   0: normal     |1: forbid|2: hidden
# resptype 0: normal     |1: the resp of resp
class TKuser(models.Model):
	user        = models.OneToOneField(User, on_delete = models.CASCADE)
	nickname    = models.CharField(max_length = 100)
	img         = models.FileField()
	pwdQuestion = models.CharField(max_length = 100)
	pwdAnswer   = models.CharField(max_length = 100)
	numPost     = models.IntegerField(default = 0)
	numScore    = models.IntegerField(default = 0)
	numCoin     = models.IntegerField(default = 0)
	usrStatus   = models.SmallIntegerField(default = 0)
	usrType     = models.SmallIntegerField(default = 0)

	def modifyPwd(self, newPwd):
		self.user.password = newPwd
		self.user.save()

	def modifyNickname(self, newNickname):
		self.nickname = newNickname
		self.save()

	def modifyImg(self, newImg):
		self.img = newImg
		self.save()

	def modifyStatus(self, usrId, newStatus):
		q = User.objects.filter(id = usrId)[0]
		q.tkuser.usrStatus = newStatus
		q.tkuser.save()

	def modifyPermission(self, usrId, newPermission):
		q = User.objects.filter(id = usrId)[0]
		q.tkuser.usrType = newPermission
		q.tkuser.save()

	def getPost(self):
		return TKpost.objects.filter(user = self.user)

	def newPost():
		pass

	def deletePost():
		pass

	def upvotePost():
		pass

	def giveCoinPost():
		pass

	def newResp():
		pass

	def deleteResp():
		pass

	def upvoteResp():
		pass

	def addClassTag(newClassTag):
		pass

	def delClassTag(classTag):
		pass


class TKpost(models.Model):
	title       = models.CharField(max_length = 100)
	content     = models.CharField(max_length = 1000)
	img         = models.FileField()
	attachment  = models.FileField()
	user        = models.ForeignKey(User, on_delete = models.CASCADE)
	time        = models.DateTimeField(default = timezone.now)
	classTag    = models.CharField(max_length = 100)
	keyword     = models.CharField(max_length = 100)
	numClick    = models.IntegerField(default = 0)
	numResp     = models.IntegerField(default = 0)
	score       = models.IntegerField(default = 0)
	coin        = models.IntegerField(default = 0)

	def downloadAttach():
		pass

	def getResp():
		pass


class TKresponse(models.Model):
	respType    = models.SmallIntegerField(default = 0)
	content     = models.CharField(max_length = 400)
	user        = models.ForeignKey(User, on_delete = models.CASCADE)
	post        = models.ForeignKey(TKpost, on_delete = models.CASCADE)
	hostId      = models.IntegerField()
	time        = models.DateTimeField(default = timezone.now)
	score       = models.IntegerField(default = 0)

	def getResp():
		pass

class TKclassTag(models.Model):
	classTagName = models.CharField(max_length = 100)

class TKhomepage:
	def newUser(username, password, email, nickname, img):
		q = User(username = username, password = password, email = email)
		q.save()
		u = TKuser(nickname = nickname, img = img, user = q)
		u.save()
	def createUserClass():
		pass
	def searchUsrByNickname():
		pass
	def searchUsrById():
		pass
	def searchPostByUsrId():
		pass
	def searchPostByKeyword():
		pass
	def searchPostByClassTag():
		pass
	def searchPostByScore():
		pass
	def searchPostByTime():
		pass
	def searchPostByTitle():
		pass
	def searchPostByContent():
		pass
	def searchRespByUsrId():
		pass
	def searchRespByPostId():
		pass
