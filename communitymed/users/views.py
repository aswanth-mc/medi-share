from urllib import request

from django.shortcuts import render,redirect
from django.contrib.auth import authenticate, login, logout

# Create your views here.

def login_view(request):
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