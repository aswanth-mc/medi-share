from django.urls import path
from . import views

urlpatterns = [
    path('register/', views.register_unit, name='register_unit'),
    path('approve/<int:unit_id>/', views.approve_unit, name='approve_unit'),
    path('dashboard/', views.unit_dashboard, name='unit_dashboard'),
    path('donations/', views.unit_donations, name='unit_donations'),
]