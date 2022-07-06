import re
from urllib.parse import urljoin

from bs4 import BeautifulSoup
from django.db import models

from .display_title import DisplayTitleMixIn
from .feed import Feed


class Post(models.Model, DisplayTitleMixIn):
    feed = models.ForeignKey(Feed, on_delete=models.CASCADE)
    title = models.CharField(max_length=1000)
    link = models.CharField(max_length=1000)
    category = models.CharField(max_length=1000, null=True, blank=True)
    inserted_date = models.DateTimeField(auto_now_add=True)
    pubDate = models.DateTimeField()
    guid = models.CharField(max_length=250, db_index=True)
    guid_is_permalink = models.BooleanField(default=False)
    author = models.CharField(max_length=1000, null=True, blank=True)
    content = models.TextField()
    description = models.TextField()

    def __str__(self):
        return self.display_title

    @property
    def processed_content(self):
        soup = BeautifulSoup(
            self.content if self.content else self.description, "html.parser"
        )
        # Remove all scripts
        [s.decompose() for s in soup("script")]
        # Replace all iframes with links
        for iframe in soup("iframe"):
            src = iframe.get("src")
            if not src:
                src = iframe.get("data-src")
            if src:
                a = soup.new_tag("a")
                a.string = "iframe"
                a["href"] = src
                iframe.replace_with(a)
            else:
                iframe.decompose()
        # Make all relative URLs absolute
        for tag in soup(href=re.compile("^/[^/]")):
            tag["href"] = urljoin(self.link, tag["href"])
        return str(soup)

    def to_json_dict(self):
        data = {}
        for k in ("id", "link", "author"):
            data[k] = getattr(self, k)
        data["title"] = self.display_title
        data["feedTitle"] = self.feed.display_title
        data["pubDate"] = str(self.pubDate)
        data["content"] = self.processed_content
        if hasattr(self, "starred"):
            data["starred"] = bool(int(self.starred)) if self.starred != None else False
        if hasattr(self, "read"):
            data["read"] = bool(int(self.read)) if self.read != None else False
        return data
