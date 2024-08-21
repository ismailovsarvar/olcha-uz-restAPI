from debug_toolbar.toolbar import debug_toolbar_urls
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include
from rest_framework.authtoken import views

from root import settings

urlpatterns = ([
                   path('admin/', admin.site.urls),
                   path('olcha-uz/', include('olchauz.urls')),
                   path('api-auth/', include('rest_framework.urls')),
                   path('api-token-auth/', views.obtain_auth_token),
                   path('api/', include('auth.urls')),
               ] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT))

urlpatterns += debug_toolbar_urls()
