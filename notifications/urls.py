from django.urls import path
from . import views

urlpatterns = [
<<<<<<< HEAD
    path("", views.notifications, name="notifications"),
    path("poll<int:last_id>/", views.poll_notifications, name="poll"),
    path(
        "mark-read/<int:notification_id>/",
        views.mark_notification_read,
        name="mark_notification_read",
    ),
    path(
        "mark-all-read/",
        views.mark_all_notifications_read,
        name="mark_all_notifications_read",
    ),
]
=======
    path('', views.notifications, name='notifications'),
    path('poll<int:last_id>/', views.poll_notifications, name='poll'),
    path('mark-read/<int:notification_id>/', views.mark_notification_read, name='mark_notification_read'),
    path('mark-all-read/', views.mark_all_notifications_read, name='mark_all_notifications_read'),
]
>>>>>>> 20d5f52ef1d7d03304aa3abc20f5e37cc8590b2c
