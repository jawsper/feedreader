from django.conf.urls import patterns, url
from feedreader import views

urlpatterns = patterns('feedreader.views',
    url( r'^$', 'index', name='index' ),
    url( r'^outline/(?P<outline_id>\d+)/$', 'outline', name='outline' ),
	url( r'^feed/favicon/(?P<feed_id>\d+)/$', views.FeedFaviconView.as_view(), name='feed_favicon' )
)
