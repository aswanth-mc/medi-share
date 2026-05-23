from django.urls import path
from . import views

urlpatterns = [
    path(
        'receive/<int:donation_id>/',
        views.receive_donation,
        name='receive_donation'
    ),
]