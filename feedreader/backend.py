from django.contrib.auth.backends import ModelBackend
from feedreader.models import UserToken

import datetime
from django.utils.timezone import utc

class TokenBackend( ModelBackend ):
	def authenticate( self, username = None, token = None ):
		"""We could authenticate the token by checking with OpenAM
		Server.  We don't do that here, instead we trust the middleware to do it.
		"""
		if not username or not token:
			return False
		try:
			token = UserToken.objects.get( user__username = username, token = token )
			if token.expire < datetime.datetime.utcnow().replace( tzinfo = utc ): # invalid token
				token.delete()
				return
		except UserToken.DoesNotExist:
			return
		# Here is a good place to map roles to Django Group instances or other features.
		return token.user