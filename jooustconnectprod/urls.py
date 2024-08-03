from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.views.static import serve
from django.urls import re_path

urlpatterns = [
    path('bungu/', admin.site.urls),
    path('', include('social.urls')),
    path('users/', include('users.urls')),
    path('messaging/', include('messaging.urls')),
    path('groups/', include('groups.urls')),
    path('notifications/', include('notifications.urls')),
]

if not settings.DEBUG:
    urlpatterns += [
        re_path(r'^media/(?P<path>.*)$', serve, {'document_root': settings.MEDIA_ROOT}),
        re_path(r'^static/(?P<path>.*)$', serve, {'document_root': settings.STATIC_ROOT}),
    ]
else:
    from django.conf.urls.static import static
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)