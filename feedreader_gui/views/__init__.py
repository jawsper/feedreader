# __init__.py
# Author: Jasper Seidel
# Date: 2013-06-24

from django.http import HttpResponse, Http404
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.conf import settings
from django.views.generic.base import View, TemplateView

from feedreader.models import Feed, ConfigStore, Outline

from feedreader.functions import main_navigation

import urllib.request, urllib.error, urllib.parse
import os

class SecureDispatchMixIn:
	@method_decorator(login_required)
	def dispatch(self, *args, **kwargs):
		return super().dispatch(*args, **kwargs)

class IndexView(SecureDispatchMixIn, TemplateView):
    template_name = 'feedreader/index.html'
    def get_context_data(self, **kwargs):
        context = super(IndexView, self).get_context_data(**kwargs)
        context['config'] = ConfigStore.getUserConfig(user=self.request.user)
        context['outline_list'] = main_navigation(self.request, False)
        return context

class OutlineView(IndexView):
    def get_context_data(self, outline_id, **kwargs):
        context = super(OutlineView, self).get_context_data(**kwargs)
        try:
            context['outline'] = Outline.objects.get(pk=outline_id)
        except Outline.DoesNotExist:
            raise Http404
        return context

class FeedFaviconView(SecureDispatchMixIn, View):
	def get( self, request, feed_id ):
		try:
			feed = Feed.objects.get( pk = feed_id )
			if feed.faviconUrl:
				icon = self.load_icon( feed.faviconUrl )
				if icon:
					return HttpResponse( icon[0], content_type = icon[1] )
		except Feed.DoesNotExist:
			pass
		
		return self.default_icon()
	
	
	def load_icon( self, url ):
		try:
			result = urllib.request.urlopen( urllib.request.Request( url, headers = { 'User-Agent': 'Chrome' } ) )
			data = result.read()
			content_type = result.headers.get( 'content-type' ) if 'content-type' in result.headers else 'text/html'
			return ( data, content_type, url )
		except Exception as e:
			print("Exception in load_icon: {0}".format(e))
			return False
	
	def default_icon( self ):
		return HttpResponse( open( os.path.join(settings.STATIC_ROOT, 'images/icons/silk/feed.png'), 'rb' ).read(), content_type = 'image/png' )

class ScriptUrls(TemplateView):
	template_name = 'feedreader/urls.js.html'
	content_type = 'application/javascript'

	def get_context_data(self, **kwargs):
		context = super(ScriptUrls, self).get_context_data(**kwargs)
		url_dict = {}
		from django.core.urlresolvers import reverse
		from django.utils.regex_helper import normalize
		from feedreader_api.api0 import urls as api_urls
		for url in api_urls.urlpatterns:
			url_dict[url.name] = normalize(url.regex.pattern)[0][0]
		context['urls'] = url_dict
		#context['latest_articles'] = Article.objects.all()[:5]
		return context
