from rest_framework import mixins, viewsets

from django.contrib.auth import get_user_model
from ..serializers.config import ConfigSerializer


class ConfigViewSet(
    mixins.UpdateModelMixin, mixins.RetrieveModelMixin, viewsets.GenericViewSet
):
    serializer_class = ConfigSerializer

    def get_object(self):
        return self.request.user

    def get_queryset(self):
        return get_user_model().objects.select_related("user_config")
