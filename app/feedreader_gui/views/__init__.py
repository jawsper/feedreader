# __init__.py
# Author: Jasper Seidel
# Date: 2013-06-24

from django.db.models import Q
from django.http import Http404
from django.views.generic.base import TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin

from feedreader.models import Outline, UserConfig


class IndexView(LoginRequiredMixin, TemplateView):
    template_name = "feedreader/index.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        config, _ = UserConfig.objects.get_or_create(user=self.request.user)
        filters = [Q(user=self.request.user)]
        if not config.show_nsfw_feeds:
            filters.append(Q(feed=None) | Q(feed__is_nsfw=False))
        context["config"] = config
        context["nodes"] = Outline.objects.select_related("feed").filter(*filters)
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
