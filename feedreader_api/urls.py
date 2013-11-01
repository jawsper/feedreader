from django.conf.urls import patterns, include, url

urlpatterns = patterns( 'feedreader_api',
	url(r'^0/', include('feedreader_api.views.api0.urls'), name='api0')
)
