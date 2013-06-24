# api0/__init__.py
# Author: Jasper Seidel
# Date: 2013-06-24

from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from feedreader.functions import HttpJsonResponse, get_unread_count
from feedreader.models import ConfigStore, Outline

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
