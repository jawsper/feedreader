import logging

from django.core.management.base import BaseCommand, CommandError

from feedreader.models import Outline
from feedreader.functions import get_unread_count

logger = logging.getLogger(__name__)

class Command(BaseCommand):
	def handle(self, *args, **options):
		for outline in Outline.objects.all():
			logger.info('Updating unread count for {}: {}'.format(outline.id, str(outline)))
			outline.unread_count = get_unread_count(outline.user, outline)
			outline.save()