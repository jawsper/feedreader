from django.db import models
from django.contrib.auth.models import User
from bs4 import BeautifulSoup

# Create your models here.

class DisplayTitleMixIn:
	@property
	def display_title(self):
		return self.title if self.title else '(no title)'

class Feed(models.Model, DisplayTitleMixIn):
	title 		= models.CharField(max_length=1000)
	xmlUrl 		= models.CharField(max_length=1000)
	htmlUrl 	= models.CharField(max_length=1000)
	faviconUrl  = models.CharField(max_length=1000, null=True, blank=True)
	lastPubDate = models.DateTimeField(null=True, blank=True)
	lastUpdated = models.DateTimeField(null=True, blank=True)
	lastStatus 	= models.CharField(max_length=1000, null=True, blank=True)
	lastETag	= models.CharField(max_length=100, null=True, blank=True)

	quirkFixNotXml = models.BooleanField(default=False)
	
	disabled	= models.BooleanField(default=False)
	
	def __str__(self):
		return self.display_title

class Outline(models.Model, DisplayTitleMixIn):
	user 	= models.ForeignKey(User)
	parent 	= models.ForeignKey('self', null=True, blank=True)
	title	= models.CharField(max_length=1000)
	feed 	= models.ForeignKey(Feed, null=True, blank=True)
	
	sort_position	= models.IntegerField(null=True, blank=True)
	
	sort_order_asc	= models.BooleanField(default=True)
	show_only_new	= models.BooleanField(default=True)

	folder_opened	= models.BooleanField(default=True)

	def __str__(self):
		return self.display_title

class Post(models.Model, DisplayTitleMixIn):
	feed 				= models.ForeignKey(Feed)
	title 				= models.CharField(max_length=1000)
	link 				= models.CharField(max_length=1000)
	category 			= models.CharField(max_length=1000, null=True, blank=True)
	pubDate 			= models.DateTimeField()
	guid 				= models.CharField(max_length=250, db_index=True)
	guid_is_permalink 	= models.BooleanField(default=False)
	author				= models.CharField(max_length=1000, null=True, blank=True)
	content 			= models.TextField()
	description 		= models.TextField()

	def __str__(self):
		return self.display_title
		
	def toJsonDict(self):
		data = {}
		for k in ('id', 'link', 'author'):
			data[k] = getattr(self, k)
		data['title'] = self.display_title
		data['feedTitle'] = self.feed.display_title
		data['pubDate'] = str(self.pubDate)
		soup = BeautifulSoup(self.content if self.content else self.description)
		[s.extract() for s in soup('script')]
		data['content'] = str(soup)
		if hasattr(self, 'starred'):
			data['starred'] = bool(int(self.starred)) if self.starred != None else False
		if hasattr(self, 'read'):
			data['read'] = bool(int(self.read)) if self.read != None else False
		return data

class UserPost(models.Model):
	user 	= models.ForeignKey(User)
	post 	= models.ForeignKey(Post)
	starred = models.BooleanField(default=False)
	read 	= models.BooleanField(default=False, db_index=True)
	
	class Meta:
		unique_together = (('user', 'post'))

	def toJsonDict(self):
		data = {}
		if self.post:
			data = self.post.toJsonDict()
		data['starred'] = self.starred if self.starred != None else False
		data['read'] = self.read if self.read != None else False
		return data

class ConfigStore(models.Model):
	key		= models.CharField(max_length=255, primary_key=True)
	user	= models.ForeignKey(User)
	value	= models.CharField(max_length=255)
	class Meta:
		unique_together = ('key', 'user')
		
	@staticmethod
	def getUserConfig(user):
		config = {}
		for line in ConfigStore.objects.filter(user=user):
			config[line.key] = line.value
		return config

from django.utils.timezone import utc
import datetime

class UserToken(models.Model):
	user	= models.ForeignKey(User)
	token	= models.CharField(max_length=255)
	expire	= models.DateTimeField()

	def expired(self):
		return self.expire < datetime.datetime.utcnow().replace(tzinfo=utc)
