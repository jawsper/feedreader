from django.urls import include, path
from django.contrib import admin
import django.contrib.auth.views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = (
    [
        path(
            "login/",
            django.contrib.auth.views.LoginView.as_view(
                redirect_authenticated_user=True
            ),
            name="login",
        ),
        path("logout/", django.contrib.auth.views.LogoutView.as_view(), name="logout"),
        path("admin/", admin.site.urls),
        path("api/", include("feedreader_api.urls")),
        path("", include("feedreader_gui.urls")),
    ]
    + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
)

if settings.DEBUG:
    import debug_toolbar

    urlpatterns = [
        path("__debug__/", include(debug_toolbar.urls)),
    ] + urlpatterns
