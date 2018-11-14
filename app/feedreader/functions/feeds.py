# functions/feeds.py
# Author: Jasper Seidel
# Date: 2013-06-29

from feedreader.models import Feed, Outline
import feedparser
from feedreader import tasks

def load_feed( feedXmlUrl ):
	data = feedparser.parse( feedXmlUrl )
	if not data:
		return
	if not data.feed:
		return
	insert_data = {}
	if data.feed.title:
		insert_data['title'] = data.feed.title
	insert_data['xmlUrl'] = feedXmlUrl
	if data.feed.link:
		insert_data['htmlUrl'] = data.feed.link
	return Feed( **insert_data )

def add_feed( user, feedXmlUrl ):
	try:
		feed = Feed.objects.get( xmlUrl = feedXmlUrl )
	except Feed.DoesNotExist:
		feed = load_feed( feedXmlUrl )
		feed.save()
	try:
		outline = Outline.objects.get( user = user, feed = feed )
	except Outline.DoesNotExist:
		outline = Outline( user = user, feed = feed, title = feed.title )
		outline.save()
	tasks.update_feed.delay(feed.pk)
	return { 'outline_id': outline.id }
