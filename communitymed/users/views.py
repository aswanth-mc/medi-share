from django.shortcuts import render, redirect
from units.models import PalliativeUnit
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth import get_user_model

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
                    return redirect('home')

        return render(request, 'login.html', {'error': 'Invalid credentials'})

    return render(request, 'login.html')




@login_required
def admin_dashboard(request):
    if request.user.role != 'admin':
        return redirect('home')
    
    pending_units = PalliativeUnit.objects.filter(is_verified=False)

    return render(request, 'admin/dashboard.html')

@login_required
def user_dashboard(request):
    if request.user.role != 'user':
        return redirect('login')
    return render(request, 'user/dashboard.html')




