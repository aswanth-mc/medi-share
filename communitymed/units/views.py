from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth import get_user_model
from .models import Palliativeunit

User = get_user_model()

def register_unit(request):
    if request.method == "POST":
        email = request.POST['email']
        password = request.POST['password']

        user = User.objects.create_user(
            username=email,
            email=email,
            password=password,
            role='unit'
        )

        Palliativeunit.objects.create(
            user=user,
            name=request.POST['name'],
            license_number=request.POST['license_number'],
            license_file=request.FILES['license_file'],
            location=request.POST['location'],
            phone=request.POST['phone']
        )

        return redirect('login')

    return render(request, 'unit_register.html')

@login_required
def approve_unit(request, unit_id):
    if request.user.role != 'admin':
        return redirect('home')

    unit = Palliativeunit.objects.get(id=unit_id)
    unit.is_verified = True
    unit.save()

    return redirect('admin_dashboard')