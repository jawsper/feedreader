from django.conf.urls import patterns, url
from feedreader import views

urlpatterns = patterns('feedreader.views',
	url( r'^$', 'index', name='index' ),
	url( r'^feed/(?P<feed_id>\d+)/favicon/$', views.FeedFaviconView.as_view(), name='feed_favicon' ),
	url( r'^outline/(?P<outline_id>\d+)/$', 'outline', name='outline' ),
	url( r'^api/0/get_option/$', 'get_option', name = 'get_option' ),
	url( r'^api/0/set_option/$', 'set_option', name = 'set_option' ),
	url( r'^api/0/outline/(?P<outline_id>\d+)/get_posts/$', 'get_posts', name = 'get_posts' ),
	url( r'^api/0/outline/(?P<outline_id>\d+)/get_data/$', 'get_outline_data', name = 'get_outline_data' ),
	url( r'^api/0/outline/(?P<outline_id>\d+)/set/$', 'outline_set', name = 'outline_set' ),
	url( r'^api/0/outline/(?P<outline_id>\d+)/mark_as_read/', 'outline_mark_as_read', name = 'outline_mark_as_read' ),
	url( r'^api/0/outline_get_unread_counts/', 'get_unread_counts', name = 'get_unread_counts' ),
	url( r'^api/0/post/(?P<post_id>\d+)/action/(?P<action>[a-z_]+)/$', views.PostActionView.as_view(), name='feed_action' )
)
