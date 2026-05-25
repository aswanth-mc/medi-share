from django.urls import path
from . import views

urlpatterns = [
    path('', views.welcome_view, name='welcome'),
    path('login/', views.user_login, name='login'),
    path('register-choice/', views.register_choice, name='register_choice'),
    path('register/', views.register_user, name='register_user'),
    path('user-dashboard/', views.user_dashboard, name='user_dashboard'),
    path('donate-medicine/', views.donate_medicine, name='donate_medicine'),
    path('my-donations/',views.my_donations,name='my_donations'),
    path('cancel-donation/<int:donation_id>/',views.cancel_donation,name='cancel_donation'),
    path('request-medicine/<int:donation_id>/', views.request_medicine, name='request_medicine'),
    path('request-status/', views.request_status, name='request_status'),
    path('profile/', views.user_profile, name='user_profile'),
    path('profile/edit/', views.user_edit_profile, name='user_edit_profile'),
    path('profile/change-password/', views.user_change_password, name='user_change_password'),
    path('logout/', views.user_logout, name='logout'),
]
