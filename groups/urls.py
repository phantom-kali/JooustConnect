from django.urls import path
from . import views

urlpatterns = [
    path('', views.groups, name='groups'),
    path('create/', views.create_group, name='create_group'),
    path('<int:group_id>/', views.group_detail, name='group_detail'),
    path('<int:group_id>/join/', views.join_group, name='join_group'),
    path('<int:group_id>/leave/', views.leave_group, name='leave_group'),
    path('<int:group_id>/manage-requests/', views.manage_group_requests, name='manage_group_requests'),
    path('<int:group_id>/post/', views.add_group_post, name='add_group_post'),
    path('<int:group_id>/messages/', views.group_messages, name='group_messages'),
    path('poll-group-messages/<int:group_id>/', views.poll_group_messages, name='poll_group_messages'),
    path('send-group-message/', views.send_group_message, name='send_group_message'),

    path('<int:group_id>/delete/', views.delete_group, name='delete_group'),
    path('<int:group_id>/remove-member/<int:user_id>/', views.remove_member, name='remove_member'),
    path('<int:group_id>/invite/', views.invite_to_group, name='invite_to_group'),

    path('redirect-to-group/<int:notification_id>/', views.redirect_to_group, name='redirect_to_group'),
]