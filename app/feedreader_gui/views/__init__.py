# __init__.py
# Author: Jasper Seidel
# Date: 2013-06-24

from django.db.models import Q
from django.http import Http404, HttpResponseRedirect, HttpResponse
from django.urls import reverse
from django.views.generic.base import View, TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin
import requests

from feedreader.models import Outline, UserConfig
from feedreader_api.api0 import urls as api_urls


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

        context["urls"] = {
            url.name: {"url": reverse(url.name)} for url in api_urls.urlpatterns
        }
        return context


class OutlineView(IndexView):
    def get_context_data(self, outline_id, **kwargs):
        context = super().get_context_data(**kwargs)
        try:
            context["outline"] = Outline.objects.get(pk=outline_id)
        except Outline.DoesNotExist:
            raise Http404
        return context


class FaviconView(LoginRequiredMixin, View):
    def get(self, request, outline_id: int):
        try:
            outline = Outline.objects.get(pk=outline_id)
            if outline.feed and outline.feed.favicon_url:
                response = requests.get(outline.feed.favicon_url)
                content_type = response.headers.get("content-type", "image/icon")
                return HttpResponse(
                    response.content,
                    content_type=content_type,
                )
        except Outline.DoesNotExist:
            pass
        return HttpResponseRedirect("/static/images/4986817c45fa2df22ddd.png")
