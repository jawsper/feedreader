from django.urls import include, path

urlpatterns = [
	path('api/', include('feedreader_api.urls')),
	path('', include('feedreader_gui.urls'))
]
