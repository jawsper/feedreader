from django.conf.urls import patterns, include, url
from django.views.decorators.cache import cache_page
from feedreader import views

urlpatterns = patterns('feedreader.views',
	url( r'^$', views.index, name='index' ),
	url( r'^feed/(?P<feed_id>\d+)/favicon/$', cache_page( 60 * 15 )( views.FeedFaviconView.as_view() ), name='feed_favicon' ),
	url( r'^api/0/', include( 'feedreader.views.api0.urls' ) )
)
