from django.urls import path
from django.views.decorators.cache import cache_page
import feedreader_gui.views as gui


urlpatterns = [
    path("outline/<int:outline_id>/", gui.OutlineView.as_view(), name="outline"),
    path("urls.js", gui.ScriptUrls.as_view(), name="script_urls"),
    path("", gui.IndexView.as_view(), name="index"),
]
