from django.urls import path
from . import views
from django.contrib.auth.views import LoginView, LogoutView

urlpatterns = [
    path('', views.home, name='home'),
    path('feed/', views.feed, name='feed'),
    path('register/', views.register, name='register'),
    path('login/', LoginView.as_view(template_name='socialapp/login.html', redirect_authenticated_user=True), name='login'),
    path('logout/', LogoutView.as_view(next_page='login'), name='logout'),

    path('post/create/', views.create_post, name='create_post'),
    path('post/<int:post_id>/increment_view/', views.increment_view_count, name='increment_view_count'),
    path('post/<int:post_id>/like/', views.like_post, name='like_post'),
    path('post/<int:post_id>/comment/', views.add_comment, name='add_comment'),
    path('delete_post/<int:post_id>/', views.delete_post, name='delete_post'),
    path('report_post/<int:post_id>/', views.report_post, name='report_post'),

    path('premium-dashboard/', views.premium_dashboard, name='premium_dashboard'),
    path('post/<int:post_id>/viewers/', views.post_viewers, name='post_viewers'),
    path('purchase-premium/', views.purchase_premium, name='purchase_premium'),

    path('add-mpesa-transaction/', views.add_mpesa_transaction, name='add_mpesa_transaction'),

    path('search-users/', views.search_users, name='search_users'),
    path('messages/', views.messages, name='messages'),
    path('get-messages/<int:user_id>/', views.get_messages, name='get_messages'),
    path('send-message/', views.send_message, name='send_message'),
    
    path('groups/', views.groups, name='groups'),
    path('groups/create/', views.create_group, name='create_group'),
    path('groups/<int:group_id>/', views.group_detail, name='group_detail'),
    path('groups/<int:group_id>/post/', views.add_group_post, name='add_group_post'),
    path('groups/<int:group_id>/messages/', views.group_messages, name='group_messages'),


    path('notifications/', views.notifications, name='notifications'),
    path('mark-notification-read/<int:notification_id>/', views.mark_notification_read, name='mark_notification_read'),
    path('settings/', views.settings, name='settings'),
]