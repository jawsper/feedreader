from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import User
from treebeard.admin import TreeAdmin
from treebeard.forms import movenodeform_factory
from .models import Outline, Feed, UserConfig


class ConfigInline(admin.StackedInline):
    model = UserConfig
    can_delete = False
    # verbose_name_plural = "configs"


class UserAdmin(BaseUserAdmin):
    inlines = [ConfigInline]


admin.site.unregister(User)
admin.site.register(User, UserAdmin)


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
