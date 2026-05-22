from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib.auth import get_user_model

User = get_user_model()


def welcome_view(request):
    return render(request, 'welcome.html')


def register_choice(request):
    return render(request, 'auth/register_choice.html')


#===============================
# USER REGISTER
#===============================

def register_user(request):
    if request.method == "POST":
        email = request.POST.get('email')
        password = request.POST.get('password')
        username = request.POST.get('username')
        phone = request.POST.get('phone')
        location_name = request.POST.get('location_name')
        latitude = request.POST.get('latitude')
        longitude = request.POST.get('longitude')

        if User.objects.filter(email=email).exists():
            return render(request, 'register.html', {
                'error': 'Email already exists'
            })
        
        user = User.objects.create_user(
            username=username,
            email=email,
            password=password,
            role='user',
            phone=phone,
            location_name=location_name,
            latitude=latitude,
            longitude=longitude
        )

        return redirect('login')
    return render(request,'register.html')


#===============================
# USER LOGIN
#===============================
def user_login(request):

    if request.method == "POST":

        email = request.POST.get('email')
        password = request.POST.get('password')

        try:
            user_obj = User.objects.get(email=email)

        except User.DoesNotExist:
            return render(
                request,
                'auth/login.html',
                {'error': 'Invalid email or password'}
            )

        user = authenticate(
            request,
            username=user_obj.username,
            password=password
        )

        if user is not None:

            login(request, user)

            if user.role == 'admin':
                return redirect('admin_dashboard')

            elif user.role == 'unit':
                return redirect('unit_dashboard')

            else:
                return redirect('user_dashboard')

        return render(
            request,
            'login.html',
            {'error': 'Invalid email or password'}
        )

    return render(request, 'auth/login.html')


#===============================
# USER DASHBOARD
#===============================

def user_dashboard(request):
    return render(request, 'dashboard.html')