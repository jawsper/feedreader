from django.urls import path
import feedreader_gui.views as gui


urlpatterns = [
    path("outline/<int:outline_id>/", gui.OutlineView.as_view(), name="outline"),
    path("", gui.IndexView.as_view(), name="index"),
]
