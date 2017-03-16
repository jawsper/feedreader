from django.core.management.base import BaseCommand
from feedreader.models import Outline, OldOutline
from feedreader.functions import IsNull

def _convert_outline_to_treeoutline(outline, tree_parent):
	return Outline(
		id=outline.id,
		user=outline.user,
		parent=tree_parent,
		title=outline.title,
		feed=outline.feed,
		sort_position=outline.sort_position,
		sort_order_asc=outline.sort_order_asc,
		folder_opened=outline.folder_opened,
		unread_count=outline.unread_count,
	)

class Command(BaseCommand):
	def handle(self, *args, **kwargs):
		Outline.objects.all().delete()
		for outline in OldOutline.objects.filter(
			parent=None
			).annotate(
			feed_is_null=IsNull('feed')
			).order_by('sort_position', '-feed_is_null', 'title'):
			tree_outline = _convert_outline_to_treeoutline(outline, None)
			print(tree_outline.id)
			tree_outline.save()
			for child_outline in outline.children.all():
				child_tree_outline = _convert_outline_to_treeoutline(child_outline, tree_outline)
				child_tree_outline.save()
			# print(outline)
			# print(tree_outline)
			# print(outline.children.all())