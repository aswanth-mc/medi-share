from django.urls import path
from . import views

urlpatterns = [
    path('register/', views.register_unit, name='register_unit'),
    path('approve/<int:unit_id>/', views.approve_unit, name='approve_unit'),
]