from django.urls import path
from . import views

urlpatterns = [
    path(
        'receive/<int:donation_id>/',
        views.receive_donation,
        name='receive_donation'
    ),
    path(
        'inventory-dashboard/',
        views.inventory_dashboard,
        name='inventory_dashboard'
    ),

]