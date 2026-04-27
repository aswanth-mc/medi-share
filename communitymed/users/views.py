from urllib import request

from django.shortcuts import render,redirect
from django.contrib.auth import authenticate, login, logout

from .models import User

# Create your views here.

def home(request):
    return render(request, 'index.html')

def user_login(request):
    if request.method == "POST":
        email = request.POST['email']
        password = request.POST['password']

        user_obj = User.objects.filter(email=email).first()

        if user_obj:
            user = authenticate(request, username=user_obj.username, password=password)

            if user:
                login(request, user)

             
                if user.role == 'admin':
                    return redirect('admin_dashboard')
                elif user.role == 'unit':
                    return redirect('unit_dashboard')
                else:
                    return redirect('home')

        return render(request, 'login.html', {'error': 'Invalid credentials'})

    return render(request, 'login.html')