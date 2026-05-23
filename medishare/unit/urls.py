from django.urls import path
from . import views

urlpatterns = [
    path('register/', views.register_unit, name='register_unit'),
    path('dashboard/', views.unit_dashboard, name='unit_dashboard'),
    path('verification-pending/', views.verification_pending, name='verification_pending'),
    path('logout/', views.unit_logout, name='unit_logout'),
]