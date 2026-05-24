from django.urls import path
from . import views

urlpatterns = [
    path('admin-dashboard/', views.admin_dashboard, name='admin_dashboard'),
    path('donations/', views.admin_donations, name='admin_donations'),
    path('remove-donation/<int:donation_id>/', views.remove_donation, name='remove_donation'),
    path('approve-unit/<int:unit_id>/', views.approve_unit, name='approve_unit'),
    path('reject-unit/<int:unit_id>/', views.reject_unit, name='reject_unit'),
    path(
    'units/',
    views.units_page,
    name='units_page'
),
    
]
