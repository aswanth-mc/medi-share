from django.urls import path
from . import views

urlpatterns = [
    path('collect-donation/<int:donation_id>/', views.collect_donation, name='collect_donation'),
]