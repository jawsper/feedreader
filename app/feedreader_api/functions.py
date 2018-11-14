from django.http import JsonResponse
from django.views.generic.base import View
from django.contrib.auth.mixins import LoginRequiredMixin


class JsonResponseView(LoginRequiredMixin, View):
    def get_response(self, user, args):
        raise NotImplementedError

    def post(self, request):
        return JsonResponse(self.get_response(request.user, request.POST))
