from django.conf.urls import url

import feedreader_api.api0 as api0
from . import auth, outline, post

urlpatterns = [
	url(r'^auth/token/$', auth.token, name='auth_token'),
	url(r'^auth/verify/$', auth.verify, name='auth_verify'),
	url(r'^feed/add/$', outline.add_feed, name='feed_add'),
	url(r'^outlines/', outline.get_all_outlines, name='outline_get_all_outlines'),
	url(r'^get_options/$', api0.get_options, name='get_options'),
	url(r'^get_unread_count/$', api0.get_unread, name='get_unread'),
	url(r'^get_option/$', api0.get_option, name = 'get_option'),
	url(r'^set_option/$', api0.set_option, name = 'set_option'),
	url(r'^outline/get_all_posts/$', outline.get_all_posts, name='get_all_posts'),
	url(r'^outline/get_starred_posts/$', outline.get_starred_posts, name='get_starred_posts'),
	url(r'^outline/get_posts/$', outline.get_posts, name='get_posts'),
	url(r'^outline/get_data/$', outline.get_outline_data, name='get_outline_data'),
	url(r'^outline/set/$', outline.outline_set, name = 'outline_set'),
	url(r'^outline/mark_as_read/$', outline.outline_mark_as_read, name='outline_mark_read'),
	url(r'^post/action/$', post.action, name='post_action')
]
