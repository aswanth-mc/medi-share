from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth import get_user_model

from inventory.models import MedicineDonation, UnitInventory
from .models import PalliativeUnit
from users.models import MedicineRequest
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

    return render(request, 'unit/unit_register.html')

@login_required
def approve_unit(request, unit_id):
    if request.user.role != 'admin':
        return redirect('home')

    unit = PalliativeUnit.objects.get(id=unit_id)
    unit.is_verified = True
    unit.save()

    return redirect('admin_dashboard')

@login_required
def unit_dashboard(request):
    if request.user.role != 'unit':
        return redirect('home')
    requests = MedicineRequest.objects.filter(user=request.user)
    return render(request, 'unit/dashboard.html', {
        'requests': requests
    })

@login_required
def unit_dashboard(request):
    if request.user.role != 'unit':
        return redirect('home')

    donations = MedicineDonation.objects.filter(status='pending')

    return render(request, 'unit/dashboard.html', {
        'donations': donations
    })

@login_required
def approve_donation(request, donation_id):
    if request.user.role != 'unit':
        return redirect('home')

    donation = MedicineDonation.objects.get(id=donation_id)
    donation.status = 'approved'
    donation.save()

    return redirect('unit_dashboard')

