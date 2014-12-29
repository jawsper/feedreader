
from django.core.management.base import BaseCommand, CommandError
from optparse import make_option

from feedreader.functions.feedupdate import FeedUpdater

class Command(BaseCommand):
	option_list = BaseCommand.option_list + (
		make_option('--debug', action='store_true', dest='debug', default=False, help='Debug'),
	)

	def handle( self, *args, **options ):
		self.stdout.write('[Feed updater]')
		self.debug = options['debug']

		updater = FeedUpdater(self.stdout)
		
		if len(args) == 1:
			updater.update_feed(range=args[0])
		else:
			updater.update_feed()

		self.stdout.write('Done! Total posts imported: {0}'.format(updater.imported))
