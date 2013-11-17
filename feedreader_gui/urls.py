from django.conf.urls import patterns, include, url
from django.views.decorators.cache import cache_page
import feedreader_gui.views as gui

urlpatterns = patterns('feedreader_gui.views',
	url(r'^$', gui.index, name='index'),
	url(r'^outline/(?P<outline_id>\d+)/$', gui.outline, name='outline'),
	url(r'^feed/(?P<feed_id>\d+)/favicon/$', cache_page(60 * 15)(gui.FeedFaviconView.as_view()), name='feed_favicon'),
	url(r'^urls.js$', gui.ScriptUrls.as_view(), name='script_urls')
)
