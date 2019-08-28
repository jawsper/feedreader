from django import template
import feedreader

register = template.Library()


@register.simple_tag
def app_version(*args, **kwargs):
	return feedreader.__version__
