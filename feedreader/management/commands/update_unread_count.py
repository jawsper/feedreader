from django.core.management.base import BaseCommand, CommandError

from feedreader.models import Outline
from feedreader.functions import get_unread_count

class Command(BaseCommand):
	def handle(self, *args, **options):
		for outline in Outline.objects.all():
			self.stdout.write('{}: {}'.format(outline.id, str(outline)))
			outline.unread_count = get_unread_count(outline.user, outline)
			outline.save()