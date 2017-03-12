from django.conf.urls import include, url

urlpatterns = [
    url(r'^0/', include('feedreader_api.api0.urls'), name='api0')
]
