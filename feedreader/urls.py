from django.conf.urls import patterns, include, url
from feedreader import views

urlpatterns = patterns('feedreader.views',
	url( r'^$', 'index', name='index' ),
	url( r'^feed/(?P<feed_id>\d+)/favicon/$', views.FeedFaviconView.as_view(), name='feed_favicon' ),
	url( r'^api/0/', include( 'feedreader.views.api0.urls' ) )
)
