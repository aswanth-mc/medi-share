from django.urls import path
from . import views

urlpatterns = [
    path('', views.welcome_view, name='welcome'),
    path('login/', views.user_login, name='login'),
    path('register-choice/', views.register_choice, name='register_choice'),
]