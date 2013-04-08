from django.conf.urls import patterns, url
from feedreader import views

urlpatterns = patterns('feedreader.views',
    url( r'^$', 'index', name='index' ),
    url( r'^outline/(?P<outline_id>\d+)/$', 'outline', name='outline' ),
	url( r'^feed/(?P<feed_id>\d+)/favicon/$', views.FeedFaviconView.as_view(), name='feed_favicon' ),
	url( r'^post/(?P<post_id>\d+)/action/(?P<action>[a-z_]+)/$', views.PostActionView.as_view(), name='feed_action' )
)
