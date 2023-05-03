from django.contrib.auth import get_user_model

from rest_framework import serializers


class ConfigSerializer(serializers.ModelSerializer):
    show_only_unread = serializers.BooleanField(source="user_config.show_only_unread")
    show_nsfw_feeds = serializers.BooleanField(source="user_config.show_nsfw_feeds")

    def update(self, instance, validated_data: dict):
        user_config = instance.user_config

        for key, value in validated_data["user_config"].items():
            setattr(user_config, key, value)
        user_config.save(update_fields=list(validated_data["user_config"].keys()))
        validated_data.pop("user_config")
        return instance

    class Meta:
        model = get_user_model()
        fields = ["show_only_unread", "show_nsfw_feeds"]
