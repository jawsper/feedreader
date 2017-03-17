from django.core.management.base import BaseCommand, CommandError

from feedreader.functions.feedupdate import FeedUpdater

class Command(BaseCommand):
	def add_arguments(self, parser):
		parser.add_argument('--debug', action='store_true', dest='debug', default=False, help='Debug')
		parser.add_argument('range')

	def handle(self, *args, **options):
		self.stdout.write('[Feed updater]')
		self.debug = options['debug']

		updater = FeedUpdater(self.stdout)
		
		if 'range' in options:
			updater.update_feed(range=options['range'])
		else:
			updater.update_feed()

		self.stdout.write('Done! Total posts imported: {0}'.format(updater.imported))
