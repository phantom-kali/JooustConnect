from django.urls import path
from django.contrib.auth.views import LoginView, LogoutView
from . import views

urlpatterns = [
    path('register/', views.register, name='register'),
    path('login/', LoginView.as_view(template_name='users/login.html', redirect_authenticated_user=True), name='login'),
    path('logout/', LogoutView.as_view(next_page='login'), name='logout'),
    path('settings/', views.settings, name='settings'),
    path('search-users/', views.search_users, name='search_users'),
    path('premium-dashboard/', views.premium_dashboard, name='premium_dashboard'),
    path('purchase-premium/', views.purchase_premium, name='purchase_premium'),
    path('add-mpesa-transaction/', views.add_mpesa_transaction, name='add_mpesa_transaction'),
]