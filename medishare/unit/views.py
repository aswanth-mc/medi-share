from django.shortcuts import render, redirect
from django.contrib.auth import authenticate
from django.contrib.auth import login
from django.contrib.auth import logout
from django.contrib.auth import get_user_model

from .models import PalliativeUnit

User = get_user_model()


# ===============================
# UNIT REGISTER
# ===============================

def register_unit(request):

    if request.method == "POST":

        username = request.POST.get('name')

        email = request.POST.get('email')

        password = request.POST.get('password')

        phone = request.POST.get('phone')

        location_name = request.POST.get('location_name')

        latitude = request.POST.get('latitude')

        longitude = request.POST.get('longitude')

        license_number = request.POST.get('license_number')

        license_file = request.FILES.get('license_file')

        # CHECK EMAIL
        if User.objects.filter(email=email).exists():

            return render(
                request,
                'registration.html',
                {
                    'error': 'Email already exists'
                }
            )

        # CREATE USER
        user = User.objects.create_user(
            username=username,
            email=email,
            password=password,
            role='unit'
        )

        # CREATE UNIT PROFILE
        PalliativeUnit.objects.create(
            user=user,

            name=username,

            email=email,

            phone=phone,

            location_name=location_name,

            latitude=latitude,

            longitude=longitude,

            license_number=license_number,

            license_file=license_file
        )

        return redirect('unit_login')

    return render(
        request,
        'registration.html'
    )


# ===============================
# UNIT LOGIN
# ===============================

def unit_login(request):

    if request.method == "POST":

        email = request.POST.get('email')

        password = request.POST.get('password')

        try:

            user_obj = User.objects.get(
                email=email,
                role='unit'
            )

        except User.DoesNotExist:

            return render(
                request,
                'unit/login.html',
                {
                    'error': 'Invalid email or password'
                }
            )

        user = authenticate(
            request,
            username=user_obj.username,
            password=password
        )

        if user is not None:

            unit = PalliativeUnit.objects.get(user=user)

            if not unit.is_verified:

                return render(
                    request,
                    'auth/login.html',
                    {
                        'error': 'Your unit is not verified yet'
                    }
                )

            login(request, user)

            return redirect('unit_dashboard')

        return render(
            request,
            'auth/login.html',
            {
                'error': 'Invalid email or password'
            }
        )

    return render(request, 'auth/login.html')


# ===============================
# UNIT DASHBOARD
# ===============================

def unit_dashboard(request):

    return render(
        request,
        'unit/dashboard.html'
    )


# ===============================
# LOGOUT
# ===============================

def unit_logout(request):

    logout(request)

    return redirect('unit_login')