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
    path('inventory/',views.inventory_dashboard,name='inventory_dashboard'),
    path('inventory/edit/<int:donation_id>/',views.edit_inventory_item,name='edit_inventory_item'),
    path('inventory/delete/<int:donation_id>/',views.delete_inventory_item,name='delete_inventory_item'),
    path('requests/', views.unit_requests, name='unit_requests'),
    path('approve-request/<int:request_id>/', views.approve_request, name='approve_request'),
    path('reject-request/<int:request_id>/', views.reject_request, name='reject_request'),
    path('collect-request/<int:request_id>/', views.collect_request, name='collect_request'),
]
