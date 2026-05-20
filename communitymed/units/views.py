from django.shortcuts import (
    render,
    redirect,
    get_object_or_404
)

from django.contrib.auth import (
    authenticate,
    login,
    logout
)

from django.contrib.auth.decorators import login_required

from django.contrib.auth import get_user_model

from django.utils import timezone

from inventory.models import (
    MedicineDonation,
    UnitInventory
)

from .models import PalliativeUnit

from users.models import MedicineRequest

User = get_user_model()


# ==============================
# UNIT REGISTER
# ==============================

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

    return render(
        request,
        'unit/unit_register.html'
    )


# ==============================
# APPROVE UNIT
# ==============================

@login_required
def approve_unit(request, unit_id):

    if request.user.role != 'admin':
        return redirect('home')

    unit = get_object_or_404(
        PalliativeUnit,
        id=unit_id
    )

    unit.is_verified = True
    unit.save()

    return redirect('admin_dashboard')


# ==============================
# UNIT DASHBOARD
# ==============================

@login_required
def unit_dashboard(request):

    if request.user.role != 'unit':
        return redirect('home')

    try:
        current_unit = request.user.palliativeunit

    except AttributeError:
        return redirect('home')

    donations = MedicineDonation.objects.filter(
        selected_unit=current_unit
    )

    incoming_requests = MedicineRequest.objects.filter(
        selected_unit__isnull=True,
        status='pending'
    )

    total_donations = donations.count()

    pending_donations = donations.filter(
        status='pending'
    ).count()

    approved_donations = donations.filter(
        status='approved'
    ).count()

    inventory_stock = UnitInventory.objects.filter(
        unit=request.user
    ).count()

    context = {

        'total_donations': total_donations,

        'pending_donations': pending_donations,

        'approved_donations': approved_donations,

        'inventory_stock': inventory_stock,

        'pending_list': donations.filter(
            status='pending'
        ).order_by('-id')[:5],

        'approved_list': donations.filter(
            status='approved'
        ).order_by('-id')[:5],

        'requests': incoming_requests.order_by('-id')[:5],
    }

    return render(
        request,
        'unit/dashboard.html',
        context
    )


# ==============================
# DONATION VIEW PAGE
# ==============================

@login_required
def unit_donations(request):

    current_unit = request.user.palliativeunit

    pending_donations = MedicineDonation.objects.filter(
        selected_unit=current_unit,
        status='pending'
    ).order_by('-created_at')

    approved_donations = MedicineDonation.objects.filter(
        selected_unit=current_unit,
        status='approved'
    ).order_by('-approved_at')

    collected_donations = MedicineDonation.objects.filter(
        selected_unit=current_unit,
        status='collected'
    ).order_by('-collected_at')

    context = {

        'pending_donations': pending_donations,

        'approved_donations': approved_donations,

        'collected_donations': collected_donations,
    }

    return render(
        request,
        'unit/donation_view.html',
        context
    )


# ==============================
# APPROVE DONATION
# ==============================

@login_required
def approve_donation(request, donation_id):

    if request.user.role != 'unit':
        return redirect('home')

    donation = get_object_or_404(
        MedicineDonation,
        id=donation_id
    )

    # SECURITY CHECK

    if donation.selected_unit != request.user.palliativeunit:
        return redirect('unit_dashboard')

    donation.status = 'approved'

    donation.approved_at = timezone.now()

    donation.save()

    return redirect('unit_donations')


# ==============================
# REJECT DONATION
# ==============================

@login_required
def reject_donation(request, donation_id):

    if request.user.role != 'unit':
        return redirect('home')

    donation = get_object_or_404(
        MedicineDonation,
        id=donation_id
    )

    # SECURITY CHECK

    if donation.selected_unit != request.user.palliativeunit:
        return redirect('unit_dashboard')

    donation.status = 'rejected'

    donation.save()

    return redirect('unit_donations')


# ==============================
# COLLECT DONATION
# ==============================

@login_required
def collect_donation(request, donation_id):

    if request.user.role != 'unit':
        return redirect('home')

    donation = get_object_or_404(
        MedicineDonation,
        id=donation_id
    )

    # SECURITY CHECK

    if donation.selected_unit != request.user.palliativeunit:
        return redirect('unit_dashboard')

    donation.status = 'collected'

    donation.collected_at = timezone.now()

    donation.save()

    # ADD TO INVENTORY

    UnitInventory.objects.create(

        unit=request.user,

        donation=donation,

        name=donation.medicine_name,

        quantity=donation.quantity,

        category=donation.category,

        expiry_date=donation.expiry_date
    )

    return redirect('unit_donations')