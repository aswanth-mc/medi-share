from urllib import request

from django.shortcuts import render,redirect
from django.contrib.auth import authenticate, login, logout

# Create your views here.
def login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user :
            login(request, user)
            if user.role == 'admin':
                return redirect('admin_dashboard')
            elif user.role == 'unit':
                return redirect('unit_dashboard')
            else: 
                return redirect('user_dashboard')
        else:
            return render(request, '/login.html', {'error': 'Invalid username or password'})
        
    return render(request, 'login.html')