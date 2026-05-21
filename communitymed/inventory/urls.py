from django.urls import path
from . import views



urlpatterns = [

    path(
        'collect/<int:donation_id>/',
        views.collect_donation,
        name='collect_donation'
    ),

    path(
        'unit-inventory/',
        views.unit_inventory,
        name='unit_inventory'
    ),

]
