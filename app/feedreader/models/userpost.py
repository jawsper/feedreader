from django.contrib.auth.models import User
from django.db import models

from .post import Post


class UserPost(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    starred = models.BooleanField(default=False)
    read = models.BooleanField(default=False, db_index=True)

    class Meta:
        unique_together = ("user", "post")

    def to_json_dict(self):
        data = {}
        if self.post:
            data = self.post.to_json_dict()
        data["starred"] = self.starred if self.starred != None else False
        data["read"] = self.read if self.read != None else False
        return data
