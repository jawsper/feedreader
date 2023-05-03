import re

from rest_framework.schemas.openapi import AutoSchema as BaseAutoSchema
from rest_framework_recursive.fields import RecursiveField


class AutoSchema(BaseAutoSchema):
    def __init__(self, tags=None, operation_id_base=None, component_name=None):
        super().__init__(tags, operation_id_base, component_name)
        self.regex = re.compile("{(.+)}")

    def map_field(self, field):
        if isinstance(field, RecursiveField) and field.proxied:
            if getattr(field.proxied, "many", False):
                return {
                    "type": "array",
                    "items": self.get_reference(field.proxied.parent),
                }
            return self.get_reference(field.proxied)
        return super().map_field(field)

    def get_serializer(self, path, method):
        if "{" in path:
            kwargs = self.regex.findall(path)
            self.view.kwargs = {kwarg: 0 for kwarg in kwargs}
        return super().get_serializer(path, method)
