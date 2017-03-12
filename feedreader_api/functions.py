from django.http import JsonResponse
from django.views.generic.base import View
from feedreader.functions import SecureDispatchMixIn


class JsonResponseView(SecureDispatchMixIn, View):
    def get_response(self, user, args):
        raise NotImplementedError

    def post(self, request):
        return JsonResponse(self.get_response(request.user, request.POST))
