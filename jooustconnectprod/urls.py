from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.views.static import serve
from django.urls import re_path

urlpatterns = [
<<<<<<< HEAD
    path("bungu/", admin.site.urls),
    path("", include("social.urls")),
    path("users/", include("users.urls")),
    path("messaging/", include("messaging.urls")),
    path("groups/", include("groups.urls")),
    path("notifications/", include("notifications.urls")),
=======
    path('bungu/', admin.site.urls),
    path('', include('social.urls')),
    path('users/', include('users.urls')),
    path('messaging/', include('messaging.urls')),
    path('groups/', include('groups.urls')),
    path('notifications/', include('notifications.urls')),
>>>>>>> 20d5f52ef1d7d03304aa3abc20f5e37cc8590b2c
]

if not settings.DEBUG:
    urlpatterns += [
<<<<<<< HEAD
        re_path(r"^media/(?P<path>.*)$", serve, {"document_root": settings.MEDIA_ROOT}),
        re_path(
            r"^static/(?P<path>.*)$", serve, {"document_root": settings.STATIC_ROOT}
        ),
    ]
else:
    from django.conf.urls.static import static

    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
=======
        re_path(r'^media/(?P<path>.*)$', serve, {'document_root': settings.MEDIA_ROOT}),
        re_path(r'^static/(?P<path>.*)$', serve, {'document_root': settings.STATIC_ROOT}),
    ]
else:
    from django.conf.urls.static import static
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
>>>>>>> 20d5f52ef1d7d03304aa3abc20f5e37cc8590b2c
