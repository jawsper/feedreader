# functions/__init__.py
# Author: Jasper Seidel
# Date: 2013-06-29

from django.http import HttpResponse, JsonResponse
from feedreader.models import Outline, Post, UserPost

import re
import json

from django.db.models.aggregates import Aggregate


class IsNull(Aggregate):
    function = "ISNULL"
    name = "IsNull"


class HttpJsonResponse(HttpResponse):
    def __init__(self, data=None, **kwargs):
        HttpResponse.__init__(
            self, json.dumps(data if data else kwargs), content_type="application/json"
        )


class JsonErrorResponse(JsonResponse):
    def __init__(self, message):
        super().__init__({"error": True, "caption": "Error", "message": message})


def get_unread_count(user, outline: Outline):
    if outline.feed:
        query = UserPost.objects.filter(
            user=outline.user, post__feed=outline.feed, read=False
        )
    else:

        feed_query = (
            outline.get_descendants()
            .filter(feed__isnull=False)
            .values_list("feed", flat=True)
        )
        post_query = Post.objects.filter(feed__in=feed_query)
        query = UserPost.objects.filter(
            user=outline.user, post__in=post_query, read=False
        )
    return query.count()


def get_total_unread_count(user):
    query = UserPost.objects.filter(user=user, read=False)
    return query.count()


def get_starred_unread_count(user):
    query = UserPost.objects.filter(user=user, starred=True)
    return query.count()


import urllib.request, urllib.error, urllib.parse


class FaviconFinder:
    def __init__(self, feed, stdout):
        self.feed = feed
        self.stdout = stdout

    def find(self):
        icon = self.find_icon_in_page()
        if icon:
            return icon[2]
        icon = self.try_force_favicon()
        if icon:
            return icon[2]

    def find_and_save(self):
        # locate the <link> tag and find the icon in there
        self.stdout.write(" * Trying to find icon in html page")
        icon = self.find_icon_in_page()
        if icon:
            self.save_icon(icon[2])
            return

        # try <host>/favicon.ico
        self.stdout.write(" * Trying <host>/favicon.ico")
        icon = self.try_force_favicon()
        if icon:
            self.save_icon(icon[2])
            return

        self.stdout.write(" * No icon found...")

    def save_icon(self, url):
        self.stdout.write(" * Found icon at {}".format(url))
        self.feed.favicon_url = url
        self.feed.save()

    def load_icon(self, url):
        try:
            result = urllib.request.urlopen(
                urllib.request.Request(url, headers={"User-Agent": "Chrome"})
            )
            data = result.read()
            content_type = (
                result.headers.get("content-type")
                if "content-type" in result.headers
                else "text/html"
            )
            return (data, content_type, url)
        except Exception as e:
            print("Exception in load_icon: {0}".format(e))
            return False

    def find_icon_in_page(self):
        # load associated html page
        try:
            data = urllib.request.urlopen(
                urllib.request.Request(
                    self.feed.html_url, headers={"User-Agent": "Chrome"}
                )
            ).read()
            matches = re.findall("<link ([^>]+)>", data)
            for match in matches:
                if re.search('rel="(shortcut )?icon"', match):
                    m = re.search('href="([^"]+)"', match)
                    if not m:
                        continue

                    favicon_url = m.groups(1)[0]

                    p_favicon_url = urllib.parse.urlparse(favicon_url)

                    # relative url, add hostname of site
                    if not p_favicon_url.hostname:
                        p_url = urllib.parse.urlparse(self.feed.html_url)
                        favicon_url = urllib.parse.urlunparse(
                            p_url[0:2] + p_favicon_url[2:]
                        )

                    return self.load_icon(favicon_url)
        except:
            pass
        return False

    def try_force_favicon(self):
        p_url = urllib.parse.urlparse(self.feed.html_url)
        return self.load_icon("{0}://{1}/favicon.ico".format(p_url[0], p_url[1]))

    def default_icon(self):
        return HttpResponse(
            open(settings.STATIC_ROOT + "images/icons/silk/feed.png", "r").read(),
            content_type="image/png",
        )


def find_favicon(feed):
    return FaviconFinder(feed, None).find()


def ensure_https_url(url: str):
    if url and url.startswith("http://"):
        url = f"https{url[4:]}"
    return url
