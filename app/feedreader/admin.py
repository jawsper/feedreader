from django.contrib import admin
from treebeard.admin import TreeAdmin
from treebeard.forms import movenodeform_factory
from .models import Outline, Feed


@admin.register(Outline)
class NewOutlineAdmin(TreeAdmin):
    form = movenodeform_factory(Outline)


@admin.register(Feed)
class FeedAdmin(admin.ModelAdmin):
    list_display = ("title", "last_updated", "last_status", "errored_since", "disabled")

    search_fields = ["title"]

    actions = ["mark_as_enabled", "mark_as_disabled"]

    def mark_as_enabled(self, request, queryset):
        queryset.update(disabled=False)

    mark_as_enabled.short_description = "Enable selected feeds"  # type: ignore

    def mark_as_disabled(self, request, queryset):
        queryset.update(disabled=True)

    mark_as_disabled.short_description = "Disable selected feeds"  # type: ignore
