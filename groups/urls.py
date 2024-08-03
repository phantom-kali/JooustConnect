from django.urls import path
from . import views

urlpatterns = [
    path('', views.groups, name='groups'),
    path('create/', views.create_group, name='create_group'),
    path('<int:group_id>/', views.group_detail, name='group_detail'),
    path('<int:group_id>/post/', views.add_group_post, name='add_group_post'),
    path('<int:group_id>/messages/', views.group_messages, name='group_messages'),
    path('poll-group-messages/<int:group_id>/', views.poll_group_messages, name='poll_group_messages'),
    path('send-group-message/', views.send_group_message, name='send_group_message'),
    path('redirect-to-group/<int:notification_id>/', views.redirect_to_group, name='redirect_to_group'),
]