# api0/__init__.py
# Author: Jasper Seidel
# Date: 2013-06-24

from feedreader.models import UserConfig
from feedreader_api.functions import JsonResponseView


class GetOptionsView(JsonResponseView):
    def get_response(self, user, args):
        config, _ = UserConfig.objects.get_or_create(user=user)
        return {
            "success": True,
            "options": {
                key: getattr(config, key) for key in UserConfig.get_config_keys()
            },
        }


class GetOptionView(JsonResponseView):
    def get_response(self, user, args):
        config, _ = UserConfig.objects.get_or_create(user=user)
        if "keys" in args:
            return {
                "success": True,
                "options": {
                    key: getattr(config, key)
                    for key in UserConfig.get_config_keys()
                    if key in args["keys"]
                },
            }

        return {
            "success": True,
            "options": {
                key: getattr(config, key) for key in UserConfig.get_config_keys()
            },
        }


class SetOptionView(JsonResponseView):
    def get_response(self, user, args):
        if len(args) == 0:
            return {"success": False, "error": True, "message": "Invalid arguments."}
        config, _ = UserConfig.objects.get_or_create(user=user)
        fields = list(args.keys())
        invalid_args = set(fields) - set(UserConfig.get_config_keys())
        if len(invalid_args) > 0:
            return {
                "success": False,
                "error": True,
                "message": f"Received invalid keys: {list(invalid_args)}",
            }
        for key, value in args.items():
            setattr(config, key, value)
        config.save(update_fields=fields)
        return {"success": True}
