# __init__.py
# Author: Jasper Seidel
# Date: 2013-06-24

from django.http import Http404
from django.views.generic.base import TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin

from feedreader.models import ConfigStore, Outline


class IndexView(LoginRequiredMixin, TemplateView):
    template_name = "feedreader/index.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["config"] = ConfigStore.getUserConfig(user=self.request.user)
        context["nodes"] = Outline.objects.select_related("feed").filter(
            user=self.request.user
        )
        return context


class OutlineView(IndexView):
    def get_context_data(self, outline_id, **kwargs):
        context = super().get_context_data(**kwargs)
        try:
            context["outline"] = Outline.objects.get(pk=outline_id)
        except Outline.DoesNotExist:
            raise Http404
        return context


class ScriptUrls(TemplateView):
    template_name = "feedreader/urls.js.html"
    content_type = "application/javascript"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        from feedreader_api.api0 import urls as api_urls

        context["urls"] = {url.name: url.pattern for url in api_urls.urlpatterns}
        return context
