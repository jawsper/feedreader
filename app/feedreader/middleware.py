from django.contrib.auth import authenticate, login
from django.http import HttpResponseForbidden


class TokenMiddleware(object):
    def process_request(self, request):
        if not hasattr(request, "user"):
            raise ImproperlyConfigured()
        if "username" not in request.POST or "token" not in request.POST:
            return
        if request.POST["username"] and request.POST["token"]:
            user = authenticate(
                username=request.POST["username"], token=request.POST["token"]
            )
            if user:
                request.user = user
                login(request, user)


class XmlHttpRequestLoginChecker(object):
    def process_request(self, request):
        if (
            "HTTP_X_REQUESTED_WITH" in request.META
            and request.META["HTTP_X_REQUESTED_WITH"] == "XMLHttpRequest"
        ):
            if not request.user.is_authenticated():
                return HttpResponseForbidden()
