from django.conf.urls import patterns, include, url

urlpatterns = patterns('feedreader.views',
	url(r'^api/0/', include('feedreader_api.views.api0.urls')),
	url(r'^', include('feedreader_gui.urls'))
)
