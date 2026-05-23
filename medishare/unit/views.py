
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required

User = get_user_model()


# ==========================================
# UNIT REGISTER
# ==========================================

def register_unit(request):

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
                'registration.html',
                {
                    'error': 'Email already exists'
                }
            )

        # CREATE UNIT USER
        unit = User.objects.create_user(
            username=username,
            email=email,
            password=password,
            role='unit',
            phone=phone,
            location_name=location_name,
            latitude=latitude,
            longitude=longitude
        )

        return redirect('unit_login')

    return render(request, 'registration.html')


# ==========================================
# UNIT LOGIN
# ==========================================

def unit_login(request):

    if request.method == "POST":

        email = request.POST.get('email')
        password = request.POST.get('password')

        try:
            user_obj = User.objects.get(email=email)

        except User.DoesNotExist:

            return render(
                request,
                'auth/login.html',
                {
                    'error': 'Invalid email or password'
                }
            )

        user = authenticate(
            request,
            username=user_obj.username,
            password=password
        )

        if user is not None and user.role == 'unit':

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


# ==========================================
# UNIT DASHBOARD
# ==========================================

@login_required 
def unit_dashboard(request): 
    if request.user.role != 'unit': 
        return redirect('login') 
    if request.user.verification_status != 'approved': 
        return render( request, 'unit/pending_approval.html' ) 
    return render( request, 'unit_dashboard.html' )


# ==========================================
# LOGOUT
# ==========================================

def unit_logout(request):

    logout(request)

    return redirect('unit_login')

