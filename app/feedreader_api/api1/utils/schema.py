from rest_framework.schemas.openapi import AutoSchema as BaseAutoSchema
from rest_framework_recursive.fields import RecursiveField


class AutoSchema(BaseAutoSchema):
    def map_field(self, field):
        if isinstance(field, RecursiveField) and field.proxied:
            if getattr(field.proxied, "many", False):
                return {
                    "type": "array",
                    "items": self.get_reference(field.proxied.parent),
                }
            return self.get_reference(field.proxied)
        return super().map_field(field)
