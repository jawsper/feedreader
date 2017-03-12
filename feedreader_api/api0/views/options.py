# api0/__init__.py
# Author: Jasper Seidel
# Date: 2013-06-24

from feedreader.models import ConfigStore
from feedreader_api.functions import JsonResponseView


class GetOptionsView(JsonResponseView):
    def get_response(self, user, args):
        return dict(
            options={x.key: x.value for x in ConfigStore.objects.filter(user=user)}
        )


class GetOptionView(JsonResponseView):
    def get_response(self, user, args):
        if 'keys[]' in args:
            return dict(success=True, options={x.key: x.value for x in ConfigStore.objects.filter(user=user, key__in=args.get('keys[]'))})
        elif 'keys' in args:
            return dict(success=True, options={x.key: x.value for x in ConfigStore.objects.filter(user=user, key__in=args['keys'])})
        if 'key' not in args:
            return dict(success=False, error='no key')
        data = ConfigStore.objects.get(user=user, key=args['key'])
        if not data:
            return {}
        return dict(success=True, key=data.key, value=data.value)


class SetOptionView(JsonResponseView):
    def get_response(self, user, args):
        if len(args) == 0:
            return dict(success=False, error=True, message='Invalid arguments.')
        for key, value in args.items():
            ConfigStore(user=user, key=key, value=value).save()
        return dict(success=True)
