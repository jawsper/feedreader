from django.core.management.base import BaseCommand, CommandError

from feedreader.models import Feed


class Command(BaseCommand):
    def add_arguments(self, parser):
        parser.add_argument(
            "--debug", action="store_true", dest="debug", default=False, help="Debug"
        )
        parser.add_argument(
            "-f",
            "--force",
            action="store_true",
            dest="force",
            default=False,
            help="Force update.",
        )
        parser.add_argument("feed_id", nargs="?")

    def handle(self, *args, feed_id=None, **options):
        self.stdout.write("[Favicon download]")
        self.debug = options["debug"]

        if feed_id:
            feed = Feed.objects.get(pk=feed_id)
            print(f"Feed: {feed.title}, {feed.favicon_url}")
            if not feed.favicon:
                feed.download_favicon()
        else:
            for feed in Feed.objects.filter(disabled=False, favicon=None):
                print(f"[{feed.pk:03d}] {feed.title}, {feed.favicon_url}")
                if not feed.favicon:
                    print(" - No icon, downloading now")
                    feed.download_favicon()
