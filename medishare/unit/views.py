from django.shortcuts import render, redirect
from django.contrib.auth import get_user_model

from user.views import User
from .models import PalliativeUnit

# Create your views here.
User = get_user_model()

# ==============================
# UNIT REGISTER
# ==============================

def register_unit(request):

    if request.method == "POST":

        email = request.POST['email']
        password = request.POST['password']

        user = User.objects.create_user(
            username=email,
            email=email,
            password=password,
            role='unit',
        )

        PalliativeUnit.objects.create(
            user=user,
            name=request.POST['name'],
            license_number=request.POST['license_number'],
            license_file=request.FILES['license_file'],
            location_name=request.POST['location_name'],
            latitude=request.POST['latitude'],
            longitude=request.POST['longitude'],
            phone=request.POST['phone'],
        )

        return redirect('login')

    return render(
        request,
        'registration.html'
    )

def unit_dashboard(request):
    return render(request, 'unit_dashboard.html')