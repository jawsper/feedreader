from django.contrib import admin
from mptt.admin import DraggableMPTTAdmin
from .models import Outline, Feed

@admin.register(Outline)
class OutlineAdmin(DraggableMPTTAdmin):
    list_display = (
        'tree_actions',
        'indented_title',
        'feed',
    )
    list_filter = (
        ('user', admin.RelatedOnlyFieldListFilter),
    )
    list_select_related = ('parent', 'user')

@admin.register(Feed)
class FeedAdmin(admin.ModelAdmin):
    list_display = ('title', 'lastUpdated', 'lastStatus', 'disabled')
