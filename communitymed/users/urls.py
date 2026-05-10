from django.urls import path
from . import views



urlpatterns = [
    path('', views.home, name='home'),
    path('login/', views.user_login, name='login'),
    path('register-choice/', views.register_choice, name='register_choice'),
    path('register-user/', views.register_user, name='register_user'),
    path('user-dashboard/', views.user_dashboard, name='user_dashboard'),
    path('admin-dashboard/', views.admin_dashboard, name='admin_dashboard'),
    path('request-medicine/', views.request_medicine, name='request_medicine'),
    path('logout/', views.user_logout, name='logout'),
    path('add_donation/', views.add_donation, name='add_donation'),
]