from django.urls import include, path
from django.contrib import admin
import django.contrib.auth.views

urlpatterns = [
    path('feedreader/login/', django.contrib.auth.views.login, name='login'),
    path('feedreader/logout/', django.contrib.auth.views.logout, name='logout'),
    path('feedreader/admin/', admin.site.urls),
    path('feedreader/api/', include('feedreader_api.urls')),
    path('feedreader/', include('feedreader_gui.urls'))
]
