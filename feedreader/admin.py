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
    list_display = ('title', 'lastUpdated', 'lastStatus', 'disabled', 'quirkFixNotXml')

    actions = ['mark_as_enabled', 'mark_as_disabled']

    def mark_as_enabled(self, request, queryset):
        queryset.update(disabled=False)
    mark_as_enabled.short_description = 'Enable selected feeds'

    def mark_as_disabled(self, request, queryset):
        queryset.update(disabled=True)
    mark_as_disabled.short_description = 'Disable selected feeds'
