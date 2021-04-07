from django.contrib.auth.backends import ModelBackend
from feedreader.models import UserToken


class TokenBackend(ModelBackend):
    def authenticate(self, username=None, token=None, **kwargs):
        """We could authenticate the token by checking with OpenAM
        Server.  We don't do that here, instead we trust the middleware to do it.
        """
        if not username or not token:
            return
        try:
            token = UserToken.objects.get(user__username=username, token=token)
            if token.expired():  # invalid token
                token.delete()
                return
        except UserToken.DoesNotExist:
            return
        # Here is a good place to map roles to Django Group instances or other features.
        return token.user
