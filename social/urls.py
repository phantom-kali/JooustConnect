from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('feed/', views.feed, name='feed'),
    path('post/create/', views.create_post, name='create_post'),
    path('post/<int:post_id>/increment_view/', views.increment_view_count, name='increment_view_count'),
    path('post/<int:post_id>/like/', views.like_post, name='like_post'),
    path('post/<int:post_id>/comment/', views.add_comment, name='add_comment'),
    path('delete_post/<int:post_id>/', views.delete_post, name='delete_post'),
    path('report_post/<int:post_id>/', views.report_post, name='report_post'),
    path('api/post/<int:post_id>/<str:detail_type>/', views.post_details, name='post_details'),
    path('post/<int:post_id>/viewers/', views.post_viewers, name='post_viewers'),
]