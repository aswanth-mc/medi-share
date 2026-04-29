from django.urls import path
from . import views



urlpatterns = [
    path('', views.home, name='home'),
    path('login/', views.user_login, name='login'),
    #path('register/', views.register, name='register'),
    path('admin-dashboard/', views.admin_dashboard, name='admin_dashboard'),
    path('approve-unit/<int:unit_id>/', views.approve_unit, name='approve_unit'),
    
]