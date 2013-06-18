from django.conf.urls import patterns, url
from feedreader import views

urlpatterns = patterns('feedreader.views',
    url( r'^$', 'index', name='index' ),
    url( r'^outline/(?P<outline_id>\d+)/$', 'outline', name='outline' ),
	url( r'^outline/(?P<outline_id>\d+)/get_posts/$', 'get_posts', name = 'get_posts' ),
	url( r'^outline/(?P<outline_id>\d+)/get_posts/skip/(?P<arg_skip>\d+)/$', 'get_posts', name = 'get_posts' ),
	url( r'^outline/(?P<outline_id>\d+)/set/$', 'outline_set', name = 'outline_set' ),
	url( r'^feed/(?P<feed_id>\d+)/favicon/$', views.FeedFaviconView.as_view(), name='feed_favicon' ),
	url( r'^post/(?P<post_id>\d+)/action/(?P<action>[a-z_]+)/$', views.PostActionView.as_view(), name='feed_action' ),
	url( r'^api/0/(?P<action>[a-z_]+)/$', 'api0', name = 'api0' )
)
