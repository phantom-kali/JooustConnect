from django.urls import path
from django.contrib.auth.views import LoginView, LogoutView
from . import views

urlpatterns = [
<<<<<<< HEAD
    path("register/", views.register, name="register"),
    path(
        "login/",
        LoginView.as_view(
            template_name="users/login.html", redirect_authenticated_user=True
        ),
        name="login",
    ),
    path("logout/", LogoutView.as_view(next_page="login"), name="logout"),
    path("settings/", views.settings, name="settings"),
    path("search-users/", views.search_users, name="search_users"),
    path("premium-dashboard/", views.premium_dashboard, name="premium_dashboard"),
    path("purchase-premium/", views.purchase_premium, name="purchase_premium"),
    path(
        "add-mpesa-transaction/",
        views.add_mpesa_transaction,
        name="add_mpesa_transaction",
    ),
    path("profile/<str:username>/", views.profile, name="profile"),
    path("profile/<str:username>/edit/", views.edit_profile, name="edit_profile"),
    path("follow/<int:user_id>/", views.follow_user, name="follow_user"),
    path("unfollow/<int:user_id>/", views.unfollow_user, name="unfollow_user"),
    path(
        "profile/<str:username>/followers/", views.user_followers, name="user_followers"
    ),
    path(
        "profile/<str:username>/following/", views.user_following, name="user_following"
    ),
]
=======
    path('register/', views.register, name='register'),
    path('login/', LoginView.as_view(template_name='users/login.html', redirect_authenticated_user=True), name='login'),
    path('logout/', LogoutView.as_view(next_page='login'), name='logout'),
    path('settings/', views.settings, name='settings'),
    path('search-users/', views.search_users, name='search_users'),
    path('premium-dashboard/', views.premium_dashboard, name='premium_dashboard'),
    path('purchase-premium/', views.purchase_premium, name='purchase_premium'),
    path('add-mpesa-transaction/', views.add_mpesa_transaction, name='add_mpesa_transaction'),

    path('profile/<str:username>/', views.profile, name='profile'),
    path('profile/<str:username>/edit/', views.edit_profile, name='edit_profile'),
    path('follow/<int:user_id>/', views.follow_user, name='follow_user'),
    path('unfollow/<int:user_id>/', views.unfollow_user, name='unfollow_user'),

    path('profile/<str:username>/followers/', views.user_followers, name='user_followers'),
    path('profile/<str:username>/following/', views.user_following, name='user_following'),

]
>>>>>>> 20d5f52ef1d7d03304aa3abc20f5e37cc8590b2c
