from django.conf.urls import patterns, include, url

urlpatterns = patterns( 'feedreader_api',
	url(r'^0/', include('feedreader_api.api0.urls'), name='api0')
)
