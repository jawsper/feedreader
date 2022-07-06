from django.contrib.auth.models import User
from django.db import models


class UserConfig(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    show_only_unread = models.BooleanField(default=True)
    show_nsfw_feeds = models.BooleanField(default=False)

    def __str__(self):
        return f"UserConfig(user={self.user}, show_only_unread={self.show_only_unread}, show_nsfw_feeds={self.show_nsfw_feeds})"

    @staticmethod
    def get_user_config(user):
        return UserConfig.objects.filter(user=user).first()

    @classmethod
    def get_config_keys(cls):
        ignore_fields = ["id", "user"]
        return [
            field.name
            for field in cls._meta.get_fields()
            if not field.name in ignore_fields
        ]

    def to_dict(self):
        return {
            "show_only_unread": self.show_only_unread,
            "show_nsfw_feeds": self.show_nsfw_feeds,
        }
