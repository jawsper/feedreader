# api0/__init__.py
# Author: Jasper Seidel
# Date: 2013-06-24

from django.http import HttpResponse, HttpResponseForbidden
from django.contrib.auth.decorators import login_required
from feedreader.functions import HttpJsonResponse, get_unread_count, get_total_unread_count
from feedreader.models import ConfigStore, Outline

import django.contrib.auth as auth

def login( request ):
	if not all( k in request.POST for k in ( 'user', 'pass' ) ): # check if username and password are supplied
		return HttpResponseForbidden()

	user = auth.authenticate( username = request.POST['user'], password = request.POST['pass'] )
	if user is not None:
		if user.is_active:
			auth.login( request, user )
			return HttpResponse( 'OK' )
		else:
			return HttpResponseForbidden()
	else:
		return HttpResponseForbidden()

@login_required
def get_options( request ):
	return HttpJsonResponse( options = { x.key: x.value for x in ConfigStore.objects.filter( user = request.user ) } )

@login_required
def get_unread( request ):
	if not 'outline_id' in request.REQUEST:
		return get_unread_counts( request )

	try:
		outline = Outline.objects.get( pk = int( request.REQUEST['outline_id'] ) )
	except Outline.DoesNotExist:
		return HttpJsonResponse()

	data = {}
	data[ outline.id ] = get_unread_count( request.user, outline )
	if outline.parent:
		data[ outline.parent.id ] = get_unread_count( request.user, outline.parent )
	else:
	    for child in Outline.objects.filter( parent = outline ):
	        data[ child.id ] = get_unread_count( request.user, child )
	return HttpJsonResponse( counts = data, total = get_total_unread_count( request.user ) )

@login_required
def get_option( request ):
	if 'keys[]' in request.POST:
		return HttpJsonResponse( options = { x.key: x.value for x in ConfigStore.objects.filter( user = request.user, key__in = request.POST.getlist( 'keys[]' ) ) } )
	if not 'key' in request.POST:
		return HttpJsonResponse( error = 'no key' )
	data = ConfigStore.objects.get( user = request.user, key = request.POST['key'] )
	if not data:
		return HttpJsonResponse()
	return HttpJsonResponse( key = data.key, value = data.value )
	
@login_required
def set_option( request ):
	if len( request.POST ) == 0:
		return HttpResponse( 'ERROR: no data' )
	for key, value in request.POST.iteritems():
		ConfigStore( user = request.user, key = key, value = value ).save()
	return HttpResponse( 'OK' )
	
@login_required
def get_unread_counts( request ):
	counts = { outline.id: get_unread_count( request.user, outline ) for outline in Outline.objects.filter( user = request.user ) }
	total = 0
	for outline in Outline.objects.filter( user = request.user, feed__isnull = False ):
		total += counts[ outline.id ]
	return HttpJsonResponse( counts = counts, total = total )
