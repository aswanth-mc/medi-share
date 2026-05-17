from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth import get_user_model
from django.db.models import Count


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
            role='unit',
        
        )

        PalliativeUnit.objects.create(
            user=user,
            name=request.POST['name'],
            license_number=request.POST['license_number'],
            license_file=request.FILES['license_file'],
            location_name=request.POST['location_name'],
            latitude=request.POST['latitude'],
            longitude=request.POST['longitude'],
            phone=request.POST['phone'],
            
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

    try:
      
        current_unit = request.user.palliativeunit
    except AttributeError:

        return redirect('home')

    donations = MedicineDonation.objects.filter(selected_unit=current_unit)

    incoming_requests = MedicineRequest.objects.filter(
        assigned_unit__isnull=True, 
        status='pending',
        # Optional: location=current_unit.location_name (to filter by area like Kozhikode)
    )

    total_donations = donations.count()
    pending_donations = donations.filter(status='pending').count()
    approved_donations = donations.filter(status='approved').count()
    inventory_stock = donations.filter(status='collected').count()

    context = {
        'total_donations': total_donations,
        'pending_donations': pending_donations,
        'approved_donations': approved_donations,
        'inventory_stock': inventory_stock,
        
        # Sliced record lists to display in summary rows
        'pending_list': donations.filter(status='pending').order_by('-id')[:5],
        'requests': incoming_requests.order_by('-id')[:5],
    }

    return render(request, 'unit/dashboard.html', context)

@login_required
def approve_donation(request, donation_id):
    if request.user.role != 'unit':
        return redirect('home')

    donation = MedicineDonation.objects.get(id=donation_id)
    donation.status = 'approved'
    donation.save()

    return redirect('unit_dashboard')



