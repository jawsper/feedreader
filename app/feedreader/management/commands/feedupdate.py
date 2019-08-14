from django.core.management.base import BaseCommand, CommandError

from feedreader.functions.feedupdate import FeedUpdater
import asyncio

class Command(BaseCommand):
    def add_arguments(self, parser):
        parser.add_argument('--debug', action='store_true', dest='debug', default=False, help='Debug')
        parser.add_argument('-f', '--force', action='store_true', dest='force', default=False, help='Force update.')
        parser.add_argument('range', nargs='?')

    def handle(self, *args, **options):
        self.stdout.write('[Feed updater]')
        self.debug = options['debug']

        updater = FeedUpdater(self.stdout, **options)
        asyncio.run(updater.run())

        self.stdout.write('Done! Total posts imported: {0}'.format(updater.imported))
