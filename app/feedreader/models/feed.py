from django.db import models
from django.core.files.base import ContentFile

import aiohttp
import asyncio
import mimetypes

from .display_title import DisplayTitleMixIn

mimetypes.init()


class Feed(models.Model, DisplayTitleMixIn):
    title = models.CharField(max_length=500)
    xml_url = models.CharField(max_length=1000)
    html_url = models.CharField(max_length=1000)
    favicon_url = models.CharField(max_length=1000, null=True, blank=True)
    favicon = models.ImageField(upload_to="favicon", null=True, blank=True)
    last_pub_date = models.DateTimeField(null=True, blank=True)
    last_updated = models.DateTimeField(null=True, blank=True)
    last_status = models.CharField(max_length=1000, null=True, blank=True)
    last_etag = models.CharField(max_length=100, null=True, blank=True)
    is_nsfw = models.BooleanField(default=False)
    errored_since = models.DateTimeField(null=True, blank=True, default=None)

    quirk_fix_invalid_publication_date = models.BooleanField(default=False)
    quirk_fix_override_encoding = models.CharField(max_length=32, null=True, blank=True)

    disabled = models.BooleanField(default=False)

    def __str__(self):
        return self.display_title

    async def fetch_favicon(self, url):
        try:
            async with aiohttp.ClientSession() as session:
                async with session.get(url) as response:
                    if response.headers["Content-Type"].startswith("image/"):
                        return response.headers, await response.read()
                    else:
                        return response.headers, None
        except Exception as e:
            return None, None

    def download_favicon(self):
        if not self.favicon_url:
            return False
        headers, content = asyncio.run(self.fetch_favicon(self.favicon_url))
        if not headers:
            return False

        content_type = headers["Content-Type"]
        if ";" in content_type:
            content_type = content_type.split(";")[0].strip()
        if not content:
            return False
        content = ContentFile(content)
        if content_type == "image/x-icon":
            extension = ".ico"
        else:
            extension = mimetypes.guess_extension(content_type, strict=False)

        if not extension:
            return False
        image_filename = f"{self.pk}{extension}"
        if self.favicon.name:
            self.favicon.delete()
        self.favicon.save(image_filename, content)
        return True

    @property
    def icon(self):
        if self.favicon and self.favicon.url:
            return self.favicon.url
