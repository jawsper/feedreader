# api0/__init__.py
# Author: Jasper Seidel
# Date: 2013-06-24

from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from feedreader.functions import HttpJsonResponse, get_total_unread_count
from feedreader.models import ConfigStore, Outline

@login_required
def get_options( request ):
	return HttpJsonResponse( options = { x.key: x.value for x in ConfigStore.objects.filter( user = request.user ) } )

@login_required
def get_unread( request ):
	if not 'outline_id' in request.POST:
		return get_unread_counts( request )

	try:
		outline = Outline.objects.get( pk = int( request.POST['outline_id'] ) )
	except Outline.DoesNotExist:
		return HttpJsonResponse()

	data = {}
	data[ outline.id ] = outline.unread_count
	if outline.parent:
		data[ outline.parent.id ] = outline.parent.unread_count
	else:
	    for child in Outline.objects.filter( parent = outline ):
	        data[ child.id ] = child.unread_count
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
	for key, value in request.POST.items():
		ConfigStore( user = request.user, key = key, value = value ).save()
	return HttpResponse( 'OK' )
	
@login_required
def get_unread_counts( request ):
	total = 0
	counts = {}
	for outline in Outline.objects.filter(user=request.user):
		counts[outline.id] = outline.unread_count
		if outline.feed:
			total += outline.unread_count
	# counts = { outline.id: outline.unread_count for outline in Outline.objects.filter( user = request.user ) }
	# for outline in Outline.objects.filter( user = request.user, feed__isnull = False ):
	# 	total += counts[ outline.id ]
	return HttpJsonResponse( counts = counts, total = total )