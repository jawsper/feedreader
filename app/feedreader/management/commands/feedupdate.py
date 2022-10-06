from django.core.management.base import BaseCommand

from feedreader.functions.feedupdate import FeedsUpdater
import asyncio


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
        parser.add_argument(
            "--all",
            action="store_true",
            dest="all",
            default=False,
            help="Update all feeds, including disabled.",
        )
        parser.add_argument("range", nargs="?")

    def handle(self, *args, **options):
        self.stdout.write("[Feed updater]")
        self.debug = options["debug"]

        updater = FeedsUpdater(self.stdout, **options)
        asyncio.run(updater.run())

        self.stdout.write("Done! Total posts imported: {0}".format(updater.imported))
