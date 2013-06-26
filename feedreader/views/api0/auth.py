# auth.py
# Author: Jasper Seidel
# Date: 2013-06-26

from django.http import HttpResponse, HttpResponseForbidden
import django.contrib.auth as auth
from feedreader.functions import HttpJsonResponse

from feedreader.models import UserToken
import datetime
from django.utils.timezone import utc

import uuid
def generate_token():
	return uuid.uuid4().get_hex()
	
def token( request ):
	if not all( k in request.POST for k in ( 'username', 'password' ) ): # check if username and password are supplied
		return HttpResponseForbidden()

	if 'password' in request.POST:
		user = auth.authenticate( username = request.POST['username'], password = request.POST['password'] )
		if user is not None:
			if user.is_active:
				token = generate_token()
				UserToken( user = user, token = token, expire = datetime.datetime.utcnow().replace( tzinfo = utc ) + datetime.timedelta( hours = 24 ) ).save()
				return HttpResponse( token )
	return HttpResponseForbidden()

def login( request ):
	if not 'username' in request.POST:
		return HttpResponseForbidden()
	if not any( k in request.POST for k in ( 'password', 'token' ) ): # check if password or token is supplied
		return HttpResponseForbidden()
		
	if 'password' in request.POST:
		user = auth.authenticate( username = request.POST['username'], password = request.POST['password'] )
		if user is not None:
			if user.is_active:
				request.session['token'] = generate_token()
				auth.login( request, user )
				return HttpResponse( request.session['token'] )
	elif 'token' in request.POST:
		return HttpResponse() if 'token' in request.session and request.session['token'] == request.POST['token'] else HttpResponseForbidden()
	return HttpResponseForbidden()

