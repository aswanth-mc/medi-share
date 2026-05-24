from django.urls import path
from . import views

urlpatterns = [
    path(
        'create/',
        views.create_donation,
        name='create_donation'
    ),
    path(
        'incoming/',
        views.incoming_donations,
        name='incoming_donations'
    ),
]