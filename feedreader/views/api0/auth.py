# auth.py
# Author: Jasper Seidel
# Date: 2013-06-26

from django.http import HttpResponse, HttpResponseForbidden
from django.contrib.auth import authenticate
from feedreader.functions import HttpJsonResponse

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
				token = generate_token()
				UserToken( user = user, token = token, expire = datetime.datetime.utcnow().replace( tzinfo = utc ) + datetime.timedelta( hours = 24 ) ).save()
				return HttpResponse( token )
	return HttpResponseForbidden()

def verify( request ):
	if all( k in request.POST for k in ( 'username', 'token' ) ):
		if verify_token( request.POST['username'], request.POST['token'] ):
			return HttpJsonResponse( success = True )
	return HttpJsonResponse( success = False )
