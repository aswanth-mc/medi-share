from django.urls import path
from . import views

urlpatterns = [
    path('admin-dashboard/', views.admin_dashboard, name='admin_dashboard'),
    path('donations/', views.admin_donations, name='admin_donations'),
    path('remove-donation/<int:donation_id>/', views.remove_donation, name='remove_donation'),
    path('approve-unit/<int:unit_id>/', views.approve_unit, name='approve_unit'),
    path('reject-unit/<int:unit_id>/', views.reject_unit, name='reject_unit'),
    path('units/', views.units_page, name='units_page'),
    path('profile/', views.admin_profile, name='admin_profile'),
    path('profile/edit/', views.admin_edit_profile, name='admin_edit_profile'),
    path('profile/change-password/', views.admin_change_password, name='admin_change_password'),
    path('donations/',views.admin_donations,name='admin_donations'),
    path('medicine-requests/',views.admin_requests,name='admin_requests'),
    path('inventory-overview/',views.inventory_overview,name='inventory_overview'),

]

