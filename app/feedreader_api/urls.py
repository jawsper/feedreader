from django.urls import include, path

urlpatterns = [
    path("0/", include("feedreader_api.api0.urls"), name="api0"),
    path("1/", include("feedreader_api.api1.urls"), name="api1"),
]
