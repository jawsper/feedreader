from django.conf.urls import patterns, include, url

urlpatterns = patterns('feedreader.views',
	url(r'^api/', include('feedreader_api.urls')),
	url(r'^', include('feedreader_gui.urls'))
)
