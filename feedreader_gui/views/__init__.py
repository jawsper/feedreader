# __init__.py
# Author: Jasper Seidel
# Date: 2013-06-24

from django.http import HttpResponse, Http404
from django.conf import settings
from django.views.generic.base import View, TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin

from feedreader.models import Feed, ConfigStore, Outline

import urllib.request
import urllib.error
import urllib.parse
import os


class IndexView(LoginRequiredMixin, TemplateView):
    template_name = 'feedreader/index.html'

    def get_context_data(self, **kwargs):
        context = super(IndexView, self).get_context_data(**kwargs)
        context['config'] = ConfigStore.getUserConfig(user=self.request.user)
        context['nodes'] = Outline.objects.filter(user=self.request.user)
        return context


class OutlineView(IndexView):
    def get_context_data(self, outline_id, **kwargs):
        context = super(OutlineView, self).get_context_data(**kwargs)
        try:
            context['outline'] = Outline.objects.get(pk=outline_id)
        except Outline.DoesNotExist:
            raise Http404
        return context


class FeedFaviconView(LoginRequiredMixin, View):
    def get(self, request, feed_id):
        if getattr(settings, 'LOAD_FAVICON', True):
            try:
                feed = Feed.objects.get(pk=feed_id)
                if feed.faviconUrl:
                    icon = self.load_icon(feed.faviconUrl)
                    if icon:
                        return HttpResponse(icon[0], content_type=icon[1])
            except Feed.DoesNotExist:
                pass

        return self.default_icon()

    def load_icon(self, url):
        try:
            result = urllib.request.urlopen(urllib.request.Request(url, headers={'User-Agent': 'Chrome'}))
            data = result.read()
            content_type = result.headers.get('content-type', 'text/html')
            return (data, content_type, url)
        except Exception as e:
            print("Exception in load_icon: {0}".format(e))
            return False

    def default_icon(self):
        return HttpResponse(open(os.path.join(settings.STATIC_ROOT, 'images/icons/silk/feed.png'), 'rb').read(), content_type='image/png')


class ScriptUrls(TemplateView):
    template_name = 'feedreader/urls.js.html'
    content_type = 'application/javascript'

    def get_context_data(self, **kwargs):
        context = super(ScriptUrls, self).get_context_data(**kwargs)
        url_dict = {}
        from django.utils.regex_helper import normalize
        from feedreader_api.api0 import urls as api_urls
        for url in api_urls.urlpatterns:
            url_dict[url.name] = normalize(url.regex.pattern)[0][0]
        context['urls'] = url_dict
        return context
