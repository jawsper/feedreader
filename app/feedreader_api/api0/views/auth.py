# auth.py
# Author: Jasper Seidel
# Date: 2013-06-26

from django.http import HttpResponse, HttpResponseForbidden
from django.contrib.auth import authenticate
from feedreader.functions import HttpJsonResponse
from feedreader.models import UserToken
from django.utils.timezone import utc
import datetime

from feedreader.functions import verify_token

import uuid
def generate_token():
	return uuid.uuid4().get_hex()

def token( request ):
	if not all( k in request.POST for k in ( 'username', 'password' ) ): # check if username and password are supplied
		return HttpResponseForbidden()

	if 'password' in request.POST:
		user = authenticate( username = request.POST['username'], password = request.POST['password'] )
		if user is not None:
			if user.is_active:
				token = None
				try:
					token = UserToken.objects.get( user = user )
					if token.expired():
						token.delete()
						token = None
				except ( UserToken.DoesNotExist, UserToken.MultipleObjectsReturned ):
					token = None
				if not token:
					raw_token = generate_token()
					token = UserToken( user = user, token = raw_token, expire = datetime.datetime.utcnow().replace( tzinfo = utc ) + datetime.timedelta( hours = 24 ) )
					token.save()
				return HttpResponse( token.token )
	return HttpResponseForbidden()

def verify( request ):
	if all( k in request.POST for k in ( 'username', 'token' ) ):
		if verify_token( request.POST['username'], request.POST['token'] ):
			return HttpJsonResponse( success = True )
	return HttpJsonResponse( success = False )
