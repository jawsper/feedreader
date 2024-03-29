# api0/post.py
# Author: Jasper Seidel
# Date: 2013-06-24

from feedreader.functions.outline import update_userpost_unread_count
from feedreader.models import Post, UserPost
from feedreader_api.functions import JsonResponseView


class PostActionView(JsonResponseView):
    def get_response(self, user, args):
        try:
            post_id = args.get("post", None)
            post = Post.objects.get(id=post_id)
        except Post.DoesNotExist:
            return {"success": False, "caption": "Error", "message": "Post not found."}

        action = args.get("action", None)
        state = args.get("state", None)
        try:
            state = bool(int(state))
        except ValueError:
            state = None
        if action not in ("starred", "read") or state is None:
            return {
                "success": False,
                "caption": "Error",
                "message": "Invalid parameters.",
            }

        try:
            user_post = UserPost.objects.select_related("user", "post").get(
                user=user, post=post
            )
        except UserPost.DoesNotExist:
            user_post = UserPost(user=user, post=post)

        changed = False
        if user_post.pk is None:
            changed = True
        else:
            current_value = getattr(user_post, action)
            if current_value != state:
                changed = True

        if changed:
            setattr(user_post, action, state)
            user_post.save(update_fields=[action])
            if action == "read":
                update_userpost_unread_count(user_post, -1 if state else +1)

            result_message = "Post {} marked as {}".format(
                post_id, action if state else "not " + action
            )
            return {"success": True, "caption": "Result", "message": result_message}

        return {
            "success": True,
            "caption": "Result",
            "message": "Post[{}].{} not changed".format(post.id, action),
        }
