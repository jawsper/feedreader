from django.conf.urls import include, url

urlpatterns = [
	url(r'^api/', include('feedreader_api.urls')),
	url(r'^', include('feedreader_gui.urls'))
]
