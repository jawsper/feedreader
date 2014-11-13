from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Feed( models.Model ):
	title 		= models.CharField( max_length = 1000 )
	xmlUrl 		= models.CharField( max_length = 1000 )
	htmlUrl 	= models.CharField( max_length = 1000 )
	faviconUrl  = models.CharField( max_length = 1000, null = True, blank = True )
	lastPubDate = models.DateTimeField( null = True, blank = True )
	lastUpdated = models.DateTimeField( null = True, blank = True )
	lastStatus 	= models.CharField( max_length = 1000, null = True, blank = True )
	
	disabled	= models.BooleanField( default = False )
	
	def __unicode__( self ):
		return self.title

	def _get_display_title(self):
		return self.title if len(self.title) > 0 else '(no title)'

	display_title = property(_get_display_title)

class Outline( models.Model ):
	user 	= models.ForeignKey( User )
	parent 	= models.ForeignKey( 'self', null = True, blank = True )
	title	= models.CharField( max_length = 1000 )
	feed 	= models.ForeignKey( Feed, null = True, blank = True )
	
	sort_position	= models.IntegerField( null = True, blank = True )
	
	sort_order_asc	= models.BooleanField( default = True )
	show_only_new	= models.BooleanField( default = True )

	folder_opened	= models.BooleanField( default = True )

	def __unicode__( self ):
		return self.title

	def _get_display_title(self):
		return self.title if len(self.title) > 0 else '(no title)'

	display_title = property(_get_display_title)

class Post( models.Model ):
	feed 				= models.ForeignKey( Feed )
	title 				= models.CharField( max_length = 1000 )
	link 				= models.CharField( max_length = 1000 )
	category 			= models.CharField( max_length = 1000, null = True, blank = True )
	pubDate 			= models.DateTimeField()
	guid 				= models.CharField( max_length = 250, db_index = True )
	guid_is_permalink 	= models.BooleanField( default = False )
	author				= models.CharField( max_length = 1000, null = True, blank = True )
	content 			= models.TextField()
	description 		= models.TextField()

	def __unicode__( self ):
		return self.title
		
	def toJsonDict( self ):
		data = {}
		for k in ( 'id', 'link', 'title', 'author' ):
			data[ k ] = ( getattr( self, k ) )
		if len(data['title']) == 0: data['title'] = '(no title)'
		data[ 'feedTitle' ] = str( self.feed.title )
		data[ 'pubDate' ] = str( self.pubDate )
		data[ 'content'] = ( self.content if self.content else self.description )
		if hasattr(self, 'starred'): data[ 'starred' ] = bool( int( self.starred ) ) if self.starred != None else False
		if hasattr(self, 'read'): data[ 'read' ] = bool( int( self.read ) ) if self.read != None else False
		return data

class UserPost( models.Model ):
	user 	= models.ForeignKey( User )
	post 	= models.ForeignKey( Post )
	starred = models.BooleanField( default = False )
	read 	= models.BooleanField( default = False )
	
	class Meta:
		unique_together = ( ( 'user', 'post' ), )

	def toJsonDict( self ):
		data = {}
		if self.post:
			data = self.post.toJsonDict()
		data[ 'starred' ] = self.starred if self.starred != None else False
		data[ 'read' ] = self.read if self.read != None else False
		return data

class ConfigStore( models.Model ):
	key		= models.CharField( max_length = 255, primary_key = True )
	user	= models.ForeignKey( User )
	value	= models.CharField( max_length = 255 )
	class Meta:
		unique_together = ( 'key', 'user' )
		
	@staticmethod
	def getUserConfig( user ):
		config = {}
		for line in ConfigStore.objects.filter( user = user ):
			config[ line.key ] = line.value
		return config

from django.utils.timezone import utc
import datetime

class UserToken( models.Model ):
	user	= models.ForeignKey( User )
	token	= models.CharField( max_length = 255 )
	expire	= models.DateTimeField()

	def expired( self ):
		return self.expire < datetime.datetime.utcnow().replace( tzinfo = utc )
