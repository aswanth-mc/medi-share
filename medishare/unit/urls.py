from django.urls import path
from . import views

urlpatterns = [
    path('register/', views.register_unit, name='register_unit'),
    path('dashboard/', views.unit_dashboard, name='unit_dashboard'),
    path('donations/', views.unit_donations, name='unit_donations'),
    path('accept-donation/<int:donation_id>/', views.accept_donation, name='accept_donation'),
    path('collect-donation/<int:donation_id>/', views.collect_donation, name='collect_donation'),
    path('verification-pending/', views.verification_pending, name='verification_pending'),
    path('logout/', views.unit_logout, name='unit_logout'),
]
