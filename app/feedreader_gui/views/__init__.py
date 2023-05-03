# __init__.py
# Author: Jasper Seidel
# Date: 2013-06-24

from django.db.models import Q
from django.http import Http404
from django.urls import reverse
from django.views.generic.base import TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin

from feedreader.models import Outline, UserConfig
from feedreader_api.api0 import urls as api_urls
from feedreader_api.api1.serializers.outline import OutlineSerializer


class IndexView(LoginRequiredMixin, TemplateView):
    template_name = "feedreader/index.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        config: UserConfig
        config, _ = UserConfig.objects.get_or_create(user=self.request.user)
        filters = [Q(user=self.request.user)]
        if not config.show_nsfw_feeds:
            filters.append(Q(feed=None) | Q(feed__is_nsfw=False))

        root_nodes: list[Outline] = (
            Outline.objects.select_related("feed").filter(*filters).get_cached_trees()
        )
        serializer = OutlineSerializer()
        context["navigation"] = [
            serializer.to_representation(node) for node in root_nodes
        ]
        context["config"] = config.to_dict()
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
