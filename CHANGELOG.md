## 2.2.1
- updated django-treebeard to 4.7.0

## 2.2.0
- feat: make HttpOnly flag on session/csrf cookies configurable
- fix: make sure to recurse into outlines when opening/closing folders
- updated dependencies

## 2.1.0
- feat: add API endpoints for all posts and starred posts
- fix: set DJANGO_ALLOWED_HOST default to "localhost" in develop settings
- fix: allow fetching openapi schema without authentication
- fix: ensure AllPosts and StarredPosts get a unique operationId
- feat: add copy-webpack-plugin to copy favicon to static/images
- feat: add starred to unread count view
- feat: create clear_sessions task
- fix: skip closed folders when navigating outlines by keyboard
- fix: make it possible to kb-navigate outlines from the bottom
- updated dependencies

## 2.0.14
- updated dependencies

## 2.0.13
- updated dependencies

## 2.0.12
- feat: also read DJANGO_ALLOWED_HOST in develop settings

## 2.0.11
- fix: another place to check for debug_toolbar import

## 2.0.10
- fix: use correct exception to check for ModuleNotFoundError

## 2.0.9
- feat: only import debug_toolbar if it's installed

## 2.0.8
- feat: update gui dependencies
- fix: add missing migration

## 2.0.7
- feat: allow setting DJANGO_SECRET_KEY or DJANGO_SECRET_KEY_PATH to pass secret key in other ways

## 2.0.6
- dep: add pytest and pytest-django to dev dependencies
- feat: add tests for Outline.get_ancestors
- fix: ensure Outline.get_ancestors(include_self=True) return self
- feat: show UserConfig in UserAdmin

## 2.0.5
- fix: set default permission for DRF to `IsAuthenticated`

## 2.0.4
- fix: Unread count for outline does not return correct counts

## 2.0.3
- feat: show post dates in relative format

## 2.0.2
- feat: remove X-Frame-Options middleware

## 2.0.1
- updated dependencies

## 2.0.0
- add new api/1/ using django-rest-framework
- feat: use content decoding algorithm from feedparser library
- feat: use os.getenv everywhere instead of os.environ.get
- feat: add caching with redis
- feat: throw FeedUpdateFailure when feed has no XML URL, make sure hostname is not None

## 1.28.4
- fix: undo last commit

## 1.28.3
- fix: throw error when no feed URL, wrap response data in StringIO

## 1.28.2
- fix: don't throw error on bozo

## 1.28.1
- feat: make more cookie vars configurable

## 1.28.0
- feat: add django-cors-headers, update redis to 4.4.x
- feat: add corsheaders app, allow configure samesite with env vars

## 1.27.1
- feat: Upgrade to python 3.11, django 4.2
- fix: make sure Outline._cached_children is a different instance for each Outline
- updated dependencies

## 1.27.0
- fix: ensure celery apps start after web has finished migrations
- feat: use libpq5 instead of libpq-dev in final container

## 1.26.6
- Use settings.AUTH_USER_MODEL for User fk

## 1.26.5
- updated dependencies

## 1.26.4
- actions: Set permissions.contents to write to allow creating releases

## 1.26.3
- switch from hub.docker.com to ghcr.io
- add missing "restart: unless-stopped" to ingress

## 1.26.2
- updated dependencies
- updated .git-blame-ignore-revs

## 1.26.1
- updated dependencies

## 1.26.0
- atomically update outline unread counts
- updated dependencies

## 1.25.1
- remove large empty div below posts and make no more posts look better

## 1.25.0
- add infinite scrolling

## 1.24.0
- read CSRF_TRUSTED_ORIGINS from env variables

## 1.23.0
- update django to 4.1
- update github workflows
- remove OldOutline
- remove django-mptt

## 1.22.1
- merge fixes from 1.21.1 and 1.21.2

## 1.22.0
- replace django-mptt with django-treebeard
- add new Outline model based on treebeard MP_Node

## 1.21.2
- add missing migration

## 1.21.1
- remove indices on OldOutline table

## 1.21.0
- add django-treebeard
- rename Outline to OldOutline
- update python to 3.10
- update postgres to 14
- updated dependencies
- change Dockerfile so code files are owned by `nobody`

## 1.20.2
- throw error when XML parsing fails

## 1.20.1
- pass missing `extra` argument to LoggerAdapter

## 1.20.0
-

## 1.19.4
- updated dependencies

## 1.19.3
-

## 1.19.2
- updated dependencies

## 1.19.1
-

## 1.19.0
-

## 1.18.1
-

## 1.18.0
-

## 1.17.1
-

## 1.17.0
-

## 1.16.0
-

## 1.15.0
-
- updated dependencies

## 1.14.1
-

## 1.14.0
-

## 1.13.0
-

## 1.12.1
-

## 1.12.0
-

## 1.11.4
-

## 1.11.3
-

## 1.11.2
-

## 1.11.1
-

## 1.11.0
-

## 1.10.4
-

## 1.10.3
-

## 1.10.2
-

## 1.10.1
-

## 1.10.0
-

## 1.9.7
-

## 1.9.6
-

## 1.9.5
-

## 1.9.4
-

## 1.9.3
-

## 1.9.2
-

## 1.9.1
-

## 1.9.0
-

## 1.8.1
-

## 1.8.0
-

## 1.7.7
-

## 1.7.6
-

## 1.7.5
-

## 1.7.4
-

## 1.7.3
-

## 1.7.2
-

## 1.7.1
-

## 1.7.0
-

## 1.6.8
-

## 1.6.7
-

## 1.6.6
-

## 1.6.5
-

## 1.6.4
-

## 1.6.3
-

## 1.6.2
-

## 1.6.1
-

## 1.6.0
-

## 1.5.5
-

## 1.5.4
-

## 1.5.3
-

## 1.5.2
-

## 1.5.1
-

## 1.5.0
-

## 1.4.16
-

## 1.4.15
-

## 1.4.14-1
-

## 1.4.14
-

## 1.4.12
-

## 1.4.11
-

## 1.4.10
-

## 1.4.9
-

## 1.4.8
-

## 1.4.7
-

## 1.4.6
-

## 1.4.5
-

## 1.4.4
-

## 1.4.3
-

## 1.4.2
-

## 1.4.1
-

## 1.4.0
-

## 1.3.2
-

## 1.3.1
-

## 1.3.0-1
-

## 1.3.0
-

## 1.2.10
-

## 1.2.9
-

## 1.2.8
-

## 1.2.7
-

## 1.2.6
-

## 1.2.5
-

## 1.2.4
-

## 1.2.3
-

## 1.2.2
-

## 1.2.1
-

## 1.2.0
-
