# api0/post.py
# Author: Jasper Seidel
# Date: 2013-06-24

from django.contrib.auth.decorators import login_required
from feedreader.functions import HttpJsonResponse
from feedreader.models import Post, UserPost

@login_required
def action( request, post_id, action ):
	try:
		post = Post.objects.get( pk = post_id )
	except Post.DoesNotExist:
		raise Http404
		
	try:
		user_post = UserPost.objects.get( user = request.user, post = post )
	except UserPost.DoesNotExist:
		user_post = UserPost( user = request.user, post = post )
		
	params = request.POST
	
	state = None
	if 'state' in params:
		state = bool( int( params['state'] ) )
	if action in ( 'starred', 'read' ):
		if state != None:
			setattr( user_post, action, state )
			user_post.save()
		return HttpJsonResponse( caption = 'Result', message = 'Post {} marked as {}'.format( post_id, action if state else 'not ' + action ), error = False )
	raise Http404
