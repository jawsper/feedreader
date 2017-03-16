from django.contrib import admin
from mptt.admin import DraggableMPTTAdmin
from .models import Outline, Feed

@admin.register(Outline)
class OutlineAdmin(DraggableMPTTAdmin):
    list_filter = (
        ('user', admin.RelatedOnlyFieldListFilter),
    )
    list_select_related = ('parent', 'user')
