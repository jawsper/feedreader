# functions/feeds.py
# Author: Jasper Seidel
# Date: 2013-06-29

from feedreader.models import Feed

def load_feed( feed ):
	pass
def add_feed( user, feedXmlUrl ):
	try:
		feed = Feed.objects.get( xmlUrl = feedXmlUrl )
	except Feed.DoesNotExist:
		feed = load_feed( feedXmlUrl )
	pass
