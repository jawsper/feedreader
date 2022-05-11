from django.urls import path
import feedreader_gui.views as gui


urlpatterns = [
    path("favicon/<int:outline_id>/", gui.FaviconView.as_view(), name="favicon"),
    path("outline/<int:outline_id>/", gui.OutlineView.as_view(), name="outline"),
    path("", gui.IndexView.as_view(), name="index"),
]
