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
    path('post/<int:post_id>/', views.post_detail, name='post_detail'),
    path('post/<int:post_id>/like/', views.like_post, name='like_post'),
    path('post/<int:post_id>/comment/', views.add_comment, name='add_comment'),

    path('search-users/', views.search_users, name='search_users'),
    path('messages/', views.messages, name='messages'),
    path('get-messages/<int:user_id>/', views.get_messages, name='get_messages'),
    path('send-message/', views.send_message, name='send_message'),
    
    path('groups/', views.groups, name='groups'),
    path('notifications/', views.notifications, name='notifications'),
    path('settings/', views.settings, name='settings'),
]