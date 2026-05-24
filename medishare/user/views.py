
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required

User = get_user_model()


# ==========================================
# WELCOME PAGE
# ==========================================

def welcome_view(request):
    return render(request, '01-welcome/welcome.html')


# ==========================================
# REGISTER CHOICE PAGE
# ==========================================

def register_choice(request):
    return render(request, '02-auth/register_choice.html')


# ==========================================
# USER REGISTER
# ==========================================

def register_user(request):

    if request.method == "POST":

        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')
        phone = request.POST.get('phone')

        location_name = request.POST.get('location_name')
        latitude = request.POST.get('latitude')
        longitude = request.POST.get('longitude')

        # CHECK EMAIL EXISTS
        if User.objects.filter(email=email).exists():

            return render(
                request,
                '05-user/registration.html',
                {
                    'error': 'Email already exists'
                }
            )

        # CREATE USER
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

    return render(request, '05-user/registration.html')


# ==========================================
# USER LOGIN
# ==========================================

def user_login(request):

    if request.method == "POST":

        email = request.POST.get('email')
        password = request.POST.get('password')

        try:
            user_obj = User.objects.get(email=email)

        except User.DoesNotExist:

            return render(
                request,
                '02-auth/login.html',
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

            login(request, user)

            # ROLE BASED REDIRECT
            if user.role == 'admin':
                return redirect('admin_dashboard')

            elif user.role == 'unit':
                return redirect('unit_dashboard')

            else:
                return redirect('user_dashboard')

        return render(
            request,
            '02-auth/login.html',
            {
                'error': 'Invalid email or password'
            }
        )

    return render(request, '02-auth/login.html')


# ==========================================
# USER DASHBOARD
# ==========================================

@login_required
def user_dashboard(request):

    if request.user.role != 'user':
        return redirect('login')

    return render(request, '05-user/dashboard.html')


# ==========================================
# LOGOUT
# ==========================================

def user_logout(request):

    logout(request)

    return redirect('login')

