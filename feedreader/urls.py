from django.conf.urls import patterns, url
from feedreader import views

urlpatterns = patterns('feedreader.views',
	url( r'^$', 'index', name='index' ),
	url( r'^feed/(?P<feed_id>\d+)/favicon/$', views.FeedFaviconView.as_view(), name='feed_favicon' ),
	url( r'^api/0/outlines/$', 'api0.outline.get_all_outlines' ),
	url( r'^api/0/get_option/$', 'api0.get_option', name = 'get_option' ),
	url( r'^api/0/set_option/$', 'api0.set_option', name = 'set_option' ),
	url( r'^api/0/outline_get_unread_counts/', 'api0.get_unread_counts', name = 'get_unread_counts' ),
	url( r'^api/0/outline/(?P<outline_id>\d+)/get_posts/$', 'api0.outline.get_posts', name = 'get_posts' ),
	url( r'^api/0/outline/(?P<outline_id>\d+)/get_data/$', 'api0.outline.get_outline_data', name = 'get_outline_data' ),
	url( r'^api/0/outline/(?P<outline_id>\d+)/set/$', 'api0.outline.outline_set', name = 'outline_set' ),
	url( r'^api/0/outline/(?P<outline_id>\d+)/mark_as_read/', 'api0.outline.outline_mark_as_read', name = 'outline_mark_as_read' ),
	url( r'^api/0/post/(?P<post_id>\d+)/action/(?P<action>[a-z_]+)/$', 'api0.post.action' ) #views.PostActionView.as_view(), name='feed_action' )
)
