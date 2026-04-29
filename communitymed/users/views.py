from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth import get_user_model
from units.models import Palliativeunit

User = get_user_model()



def home(request):
    return render(request, 'index.html')


# 🔐 Login (Email + Password)
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

                # 🔥 Role-based redirect
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
    
    unit = PalliativeUnit.objects.get(id=unit_id)
    unit.is_verified = True
    unit.save()

    return render(request, 'admin/dashboard.html')






