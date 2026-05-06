from django.shortcuts import render, redirect
from units.models import PalliativeUnit
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth import get_user_model
from .models import MedicineRequest

User = get_user_model()



def home(request):
    return render(request, 'index.html')



def user_login(request):
    if request.method == "POST":
        email = request.POST.get('email')
        password = request.POST.get('password')

        
        user_obj = User.objects.filter(email=email).first()

        if user_obj:
            
            user = authenticate(
                request,
                username=user_obj.username,
                password=password
            )

            if user:
                login(request, user)

                
                if user.role == 'admin':
                    return redirect('admin_dashboard')
                elif user.role == 'unit':
                    return redirect('unit_dashboard')
                else:
                    return redirect('user_dashboard')

        return render(request, 'login.html', {'error': 'Invalid credentials'})

    return render(request, 'login.html')




@login_required
def admin_dashboard(request):
    if request.user.role != 'admin':
        return redirect('home')
    
    pending_units = PalliativeUnit.objects.filter(is_verified=False)

    return render(request, 'admin-temp/dashboard.html', {'pending_units': pending_units})

def register_choice(request):
    return render(request, 'register_choice.html')

def register_user(request):
    if request.method == "POST":
        email = request.POST.get('email')
        password = request.POST.get('password')
        username = request.POST.get('username')
        phone = request.POST.get('phone')
        location = request.POST.get('location')

        if User.objects.filter(email=email).exists():
            return render(request, 'user/register.html', {
                'error': 'Email already exists'
            })
        
        user = User.objects.create_user(
            username=username,
            email=email,
            password=password,
            role='user',
            phone=phone,
            location=location
        )

        return redirect('login')
    return render(request,'user/register.html')


@login_required
def user_dashboard(request):
    if request.user.role != 'user':
        return redirect('login')
    return render(request, 'user/dashboard.html')


def user_logout(request):
    logout(request)
    return redirect('home')


@login_required
def request_medicine(request):
    if request.user.role != 'user':
        return redirect('home')

    if request.method == "POST":
        medicine_name = request.POST.get('medicine_name')
        quantity = request.POST.get('quantity')
        category = request.POST.get('category') 
       

        MedicineRequest.objects.create(
            user=request.user,
            medicine_name=medicine_name,
            quantity=quantity,
            category=category,  

        )

        return redirect('user_dashboard')

    return render(request, 'user/request_medicine.html')