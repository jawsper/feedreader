import asyncio
import datetime
import logging
import re
from typing import List, Union
from asgiref.sync import sync_to_async
from time import mktime
from urllib.parse import urlparse
from wsgiref.handlers import format_date_time

import aiohttp
import feedparser

from django.db import IntegrityError
from django.utils import timezone

from feedreader import __version__
from feedreader.functions.outline import update_outline_unread_count
from feedreader.models import Feed, Post, Outline, UserPost

logger = logging.getLogger(__name__)  # pylint: disable=invalid-name


def struct_time_to_aware_datetime(time):
    return datetime.datetime(*time[:6]).replace(tzinfo=timezone.utc)


class FeedUpdateFailure(Exception):
    def __init__(self, message):
        self.message = message


class FeedsUpdater:
    def __init__(self, stdout=None, **options):
        self.stdout = stdout
        self.imported = 0
        self.options = options
        self.session = None

    def _get_session(self):
        if not self.session:
            self.session = aiohttp.ClientSession(
                headers={
                    "Connection": "close",
                    "A-IM": "feed",  # RFC 3229 support
                    "User-Agent": f"feedreader/{__version__}+https://github.com/jawsper/feedreader",
                    "Accept": "application/atom+xml,application/rdf+xml,application/rss+xml,application/x-netcdf,application/xml;q=0.9,text/xml;q=0.2,*/*;q=0.1",
                }
            )
        return self.session

    async def run(self):
        range_ = self.options.get("range", None)
        all = self.options.get("all", False)
        qs = await self.get_queryset(range_=range_, all=all)
        if qs:
            async with self._get_session() as session:
                result = await asyncio.gather(
                    *(FeedUpdater(feed, session, self.options)() for feed in qs)
                )
                self.imported += sum(result)

    @sync_to_async
    def get_queryset(
        self, *, range_: Union[str, None] = None, all: bool = False
    ) -> List:
        filter_params = {}
        if range_:
            if re.match(r"^\d+$", range_):
                filter_params["pk"] = int(range_)
            else:
                if m := re.match(r"^(\d+),$", range_):
                    filter_params["id__gte"] = int(m.group(1))
        else:
            if not all:
                filter_params["disabled"] = False

        return list(Feed.objects.filter(**filter_params))

    async def update_feed(self, feed: Feed):
        async with self._get_session() as session:
            self.imported += await FeedUpdater(feed, session, self.options)()


class FeedUpdater:
    def __init__(self, feed: Feed, session: aiohttp.ClientSession, options):
        self.imported = 0
        self.feed = feed
        self.session = session
        self.options = options

        class LoggerAdapter(logging.LoggerAdapter):
            def process(self, msg, kwargs):
                return f"[{feed.xml_url}] {msg}", kwargs

        self.log = LoggerAdapter(logger=logger.getChild(f"{feed.pk}"), extra=None)

    async def __call__(self):
        await self._update_feed()
        return self.imported

    async def _update_feed(self):
        update_fields = ["last_updated", "last_status"]
        try:
            if result := await self.load_feed():
                self.feed.last_updated = timezone.now()
                self.feed.last_status = result
                if self.feed.errored_since:
                    self.feed.errored_since = None
                    update_fields.append("errored_since")
                await sync_to_async(self.feed.save)(update_fields=update_fields)
        except FeedUpdateFailure as e:
            self.feed.last_updated = timezone.now()
            self.feed.last_status = e.message
            if not self.feed.errored_since:
                self.feed.errored_since = timezone.now()
                update_fields.append("errored_since")
            await sync_to_async(self.feed.save)(update_fields=update_fields)
        except Exception as e:
            self.log.exception("Unexpected feed error")

    async def download_feed(self):
        if not self.feed.xml_url:
            return None, None
        headers = {}
        if not self.options.get("force", False):
            if self.feed.last_etag:
                headers["If-None-Match"] = self.feed.last_etag
            modified = (
                self.feed.last_pub_date
                if self.feed.last_pub_date
                else self.feed.last_updated
            )
            if modified:
                if_modified_since = mktime(modified.timetuple())
                headers["If-Modified-Since"] = format_date_time(if_modified_since)

        # Fix for GDPR wall on tumblr sites (#14)
        hostname = urlparse(self.feed.xml_url).hostname
        if hostname.endswith(".tumblr.com"):
            headers[
                "User-Agent"
            ] = "Mozilla/5.0 (compatible; Baiduspider; +http://www.baidu.com/search/spider.html)"
        try:
            async with self.session.get(self.feed.xml_url, headers=headers) as response:
                if self.feed.quirk_fix_override_encoding is not None:
                    self.log.info(
                        "Encoding overriden to %s",
                        self.feed.quirk_fix_override_encoding,
                    )
                return (
                    await response.text(encoding=self.feed.quirk_fix_override_encoding)
                ), response
        except aiohttp.ClientConnectionError as e:
            self.log.warning("Connection error | %s", str(e))
            raise FeedUpdateFailure(f"Error in connection | {e}")
        except aiohttp.ClientResponseError as e:
            self.log.warning("Response error | %s %s", e.status, e.response)
            raise FeedUpdateFailure(f"Error in response | {e.status} {e.response}")
        except (asyncio.TimeoutError, aiohttp.ClientError) as e:
            self.log.exception("Timeout or client error | %s", str(e))
            raise FeedUpdateFailure(f"Error | {e}")

    async def load_feed(self):
        self.log.info("Loading feed")
        raw_data, response = await self.download_feed()

        if not response:
            return f"Error | unknown error"

        if response.status >= 400:
            self.log.warning("Failed: status error %s", response.status)
            raise FeedUpdateFailure(f"Error in response | {response.status}")
        elif response.status == 304:
            self.log.info("304 Not Changed")
            if not self.options.get("force", False):
                return "Success | 304"

        data = feedparser.parse(raw_data)

        if not data:
            self.log.warning("Failed: no data")
            raise FeedUpdateFailure("Error | No data")
        if data["bozo"]:
            self.log.warning("Failed to parse XML strictly: %s", data["bozo_exception"])

        if etag := response.headers.get("etag"):
            if self.feed.last_etag != etag:
                self.feed.last_etag = etag
                await sync_to_async(self.feed.save)(update_fields=["last_etag"])

        changed = True
        last_updated = None

        if "feed" in data and "updated_parsed" in data["feed"]:
            last_updated = data["feed"]["updated_parsed"]
        elif "feed" in data and "published_parsed" in data["feed"]:
            last_updated = data["feed"]["published_parsed"]
        elif "updated_parsed" in data:
            last_updated = data["updated_parsed"]
        elif "published_parsed" in data:
            last_updated = data["published_parsed"]

        if last_updated:
            last_updated = struct_time_to_aware_datetime(last_updated)

        if self.feed.quirk_fix_invalid_publication_date:
            pass
        elif (
            self.feed.last_pub_date
            and last_updated
            and self.feed.last_pub_date == last_updated
        ):
            changed = False
        elif last_updated:
            self.feed.last_pub_date = last_updated
            await sync_to_async(self.feed.save)(update_fields=["last_pub_date"])

        if not changed:
            self.log.info("No changes detected")
            if not self.options.get("force", False):
                return f"Success | No changes"

        self.log.info(
            "Scanning %d posts, please have patience...", len(data["entries"])
        )

        outlines: List[Outline] = await sync_to_async(list)(
            Outline.objects.filter(feed=self.feed).prefetch_related("user")
        )

        imported = 0

        for entry in reversed(data["entries"]):
            insert_data = {}
            if "title" in entry:
                insert_data["title"] = entry["title"]

            if "author_detail" in entry and "name" in entry["author_detail"]:
                insert_data["author"] = entry["author_detail"]["name"]

            if "links" in entry:
                if len(entry["links"]) == 0:
                    pass
                elif len(entry["links"]) == 1:
                    insert_data["link"] = entry["links"][0]["href"]
                else:
                    for link in entry["links"]:
                        if link["rel"] == "self":
                            insert_data["link"] = link["href"]
                            break

            if "link" not in insert_data:
                if "link" in entry:
                    insert_data["link"] = entry["link"]
                else:
                    self.log.warning("Can't find a link.")
                    continue

            if "content" in entry:
                insert_data["content"] = entry["content"][0]["value"]
            if "description" in entry:
                insert_data["description"] = entry["description"]
            if "published_parsed" in entry and entry["published_parsed"]:
                try:
                    insert_data["pubDate"] = struct_time_to_aware_datetime(
                        entry["published_parsed"]
                    )
                except TypeError:
                    self.log.warning("Invalid date: %s", entry["published_parsed"])
                    continue
            elif "updated_parsed" in entry and entry["updated_parsed"]:
                insert_data["pubDate"] = struct_time_to_aware_datetime(
                    entry["updated_parsed"]
                )

            if "id" in entry:
                insert_data["guid"] = entry["id"]
            if "guid" not in insert_data:
                if "pubDate" in insert_data:
                    insert_data["guid"] = insert_data["pubDate"]
                elif "link" in insert_data:
                    insert_data["guid"] = insert_data["link"]
                elif "description" in insert_data:
                    insert_data["guid"] = insert_data["description"]
                else:
                    self.log.warning(
                        "Cannot find a good unique ID %s %s", entry, str(insert_data)
                    )
                    continue
            if "pubDate" not in insert_data:
                insert_data["pubDate"] = timezone.now()

            try:
                _ = await sync_to_async(Post.objects.get)(
                    guid__exact=insert_data["guid"]
                )
            except Post.MultipleObjectsReturned:
                self.log.warning("Duplicate post! %s", str(insert_data))
            except Post.DoesNotExist:
                post = Post(**insert_data, feed=self.feed)
                try:
                    await sync_to_async(post.save)()
                    for outline in outlines:
                        await sync_to_async(update_outline_unread_count)(outline, 1)
                        # make userposts for all users who have this feed
                        up = UserPost(user=outline.user, post=post)
                        await sync_to_async(up.save)()
                    imported += 1
                except IntegrityError:
                    self.log.exception("IntegrityError %s", entry)
                    continue

        if self.feed.quirk_fix_invalid_publication_date:
            await self._fix_invalid_publication_date()

        self.log.info("Inserted %d new posts", imported)
        self.imported += imported
        return f"Success | {imported} posts added"

    @sync_to_async
    def _fix_invalid_publication_date(self):
        try:
            (self.feed.last_pub_date,) = (
                self.feed.post_set.order_by("-pubDate").values_list("pubDate").first()
            )
            self.feed.save(update_fields=["last_pub_date"])
        except IndexError:
            pass
