from django.urls import include, path
from django.contrib import admin
import django.contrib.auth.views

urlpatterns = [
    path('login/', django.contrib.auth.views.LoginView.as_view(redirect_authenticated_user=True), name='login'),
    path('logout/', django.contrib.auth.views.LogoutView.as_view(), name='logout'),
    path('admin/', admin.site.urls),
    path('api/', include('feedreader_api.urls')),
    path('', include('feedreader_gui.urls'))
]
