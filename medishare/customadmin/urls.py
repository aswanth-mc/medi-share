from django.urls import path
from . import views

urlpatterns = [
    path('admin-dashboard/', views.admin_dashboard, name='admin_dashboard'),
    path('approve-unit/<int:unit_id>/', views.approve_unit, name='approve_unit'),
    path('reject-unit/<int:unit_id>/', views.reject_unit, name='reject_unit'),
    
]