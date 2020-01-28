# functions/feeds.py
# Author: Jasper Seidel
# Date: 2013-06-29

from feedreader.models import Feed, Outline
import feedparser
from feedreader import tasks
from urllib.parse import urlparse

def load_feed(feed_xml_url):
    hostname = urlparse(feed_xml_url).hostname
    agent = None
    if hostname.endswith('.tumblr.com'):
        agent = 'Mozilla/5.0 (compatible; Baiduspider; +http://www.baidu.com/search/spider.html)'
    data = feedparser.parse(feed_xml_url, agent=agent)
    if not data:
        return
    if not data.feed:
        return
    insert_data = {}
    if data.feed.title:
        insert_data['title'] = data.feed.title
    insert_data['xml_url'] = feed_xml_url
    if data.feed.link:
        insert_data['html_url'] = data.feed.link
    return Feed(**insert_data)

def add_feed(user, feed_xml_url):
    try:
        feed = Feed.objects.get(xml_url=feed_xml_url)
    except Feed.DoesNotExist:
        feed = load_feed(feed_xml_url)
        feed.save()
    outline, created = Outline.objects.get_or_create(user=user, feed=feed, defaults=dict(title=feed.title))
    tasks.download_feed_favicon.delay(feed.pk)
    tasks.update_feed.delay(feed.pk)
    return { 'outline_id': outline.id }
