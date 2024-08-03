from django.urls import path
from . import views

urlpatterns = [
    path('', views.notifications, name='notifications'),
    path('poll<int:last_id>/', views.poll_notifications, name='poll'),
    path('mark-read/<int:notification_id>/', views.mark_notification_read, name='mark_notification_read'),
    path('mark-all-read/', views.mark_all_notifications_read, name='mark_all_notifications_read'),
]