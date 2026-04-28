from django.shortcuts import render, redirect
from django.contrib.auth import get_user_model
from .models import PalliativeUnit

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

        PalliativeUnit.objects.create(
            user=user,
            name=request.POST['name'],
            license_number=request.POST['license_number'],
            license_file=request.FILES['license_file'],
            location=request.POST['location'],
            phone=request.POST['phone']
        )

        return redirect('login')

    return render(request, 'unit_register.html')