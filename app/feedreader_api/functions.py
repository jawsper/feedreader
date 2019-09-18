from django.http import JsonResponse
from django.views.generic.base import View
from django.contrib.auth.mixins import LoginRequiredMixin
from django.conf import settings
from json import loads

class JsonResponseView(LoginRequiredMixin, View):
    raise_exception = True

    def get_response(self, user, args):
        raise NotImplementedError

    def post(self, request):
        if request.method == 'POST' and request.content_type == 'application/json':
            encoding = request.encoding if request.encoding is not None else settings.DEFAULT_CHARSET
            request_body = loads(request.body.decode(encoding))
        else:
            request_body = request.POST
        return JsonResponse(self.get_response(request.user, request_body))
