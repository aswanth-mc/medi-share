from django.contrib.auth import login, logout
from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from django.db import transaction
from django.shortcuts import get_object_or_404, render, redirect

from unit.models import PalliativeUnit
from user.models import MedicineDonation

User = get_user_model()


# ==========================================
# UNIT REGISTER
# ==========================================

def register_unit(request):

    if request.method == "POST":

        username = request.POST.get('name')
        email = request.POST.get('email')
        password = request.POST.get('password')
        phone = request.POST.get('phone')

        location_name = request.POST.get('location_name')
        latitude = request.POST.get('latitude')
        longitude = request.POST.get('longitude')

        license_number = request.POST.get('license_number')
        license_file = request.FILES.get('license_file')

        # CHECK EMPTY USERNAME
        if not username:
            return render(
                request,
                '04-unit/registration.html',
                {
                    'error': 'Unit name is required'
                }
            )

        if not email:
            return render(
                request,
                '04-unit/registration.html',
                {
                    'error': 'Email is required'
                }
            )

        # CHECK EMAIL EXISTS
        if User.objects.filter(email=email).exists():

            return render(
                request,
                '04-unit/registration.html',
                {
                    'error': 'Email already exists'
                }
            )

        if User.objects.filter(username=username).exists():
            return render(
                request,
                '04-unit/registration.html',
                {
                    'error': 'Unit name already exists'
                }
            )

        if not license_file:
            return render(
                request,
                '04-unit/registration.html',
                {
                    'error': 'Verification document is required'
                }
            )

        with transaction.atomic():
            # CREATE AUTH USER
            user = User.objects.create_user(
                username=username,
                email=email,
                password=password,
                role='unit'
            )

            # CREATE UNIT PROFILE
            PalliativeUnit.objects.create(
                user=user,
                name=username,
                email=email,
                phone=phone,
                location_name=location_name,
                latitude=latitude if latitude else None,
                longitude=longitude if longitude else None,
                license_number=license_number,
                license_file=license_file,
                is_verified=False
            )

        login(request, user)

        return redirect('verification_pending')

    return render(request, '04-unit/registration.html')


# ==========================================
# UNIT DASHBOARD
# ==========================================

@login_required
def unit_dashboard(request):

    if request.user.role != 'unit':
        return redirect('login')

    try:
        unit = PalliativeUnit.objects.get(user=request.user)

    except PalliativeUnit.DoesNotExist:
        return redirect('login')

    # CHECK VERIFIED
    if not unit.is_verified:
        return redirect('verification_pending')

    pending_donations = MedicineDonation.objects.filter(status='pending', unit=unit)[:5]
    accepted_donations = MedicineDonation.objects.filter(unit=unit, status='accepted')
    collected_donations = MedicineDonation.objects.filter(unit=unit, status='collected')

    return render(
        request,
        '04-unit/dashboard.html',
        {
            'unit': unit,
            'pending_list': pending_donations,
            'total_donations': accepted_donations.count() + collected_donations.count(),
            'pending_donations': MedicineDonation.objects.filter(status='pending', unit=unit).count(),
            'inventory_stock': collected_donations.count(),
            'expiring_soon': accepted_donations.count(),
        }
    )


# ==========================================
# VERIFICATION PENDING
# ==========================================

@login_required
def verification_pending(request):

    if request.user.role != 'unit':
        return redirect('login')

    return render(
        request,
        '04-unit/verification_pending.html'
    )


# ==========================================
# UNIT DONATIONS
# ==========================================

@login_required
def unit_donations(request):

    if request.user.role != 'unit':
        return redirect('login')

    try:
        unit = PalliativeUnit.objects.get(user=request.user)

    except PalliativeUnit.DoesNotExist:
        return redirect('login')

    if not unit.is_verified:
        return redirect('verification_pending')

    pending_donations = MedicineDonation.objects.filter(status='pending', unit=unit)
    unit_donations = MedicineDonation.objects.filter(unit=unit).exclude(status='removed')

    return render(
        request,
        '04-unit/incoming_donations.html',
        {
            'unit': unit,
            'pending_donations': pending_donations,
            'unit_donations': unit_donations,
        }
    )


# ==========================================
# ACCEPT DONATION
# ==========================================

@login_required
def accept_donation(request, donation_id):

    if request.user.role != 'unit':
        return redirect('login')

    unit = get_object_or_404(PalliativeUnit, user=request.user, is_verified=True)
    donation = get_object_or_404(
        MedicineDonation,
        id=donation_id,
        status='pending',
        unit=unit,
    )

    if request.method == "POST":
        donation.unit = unit
        donation.status = 'accepted'
        donation.save()

    return redirect('unit_donations')


# ==========================================
# MARK DONATION COLLECTED
# ==========================================

@login_required
def collect_donation(request, donation_id):

    if request.user.role != 'unit':
        return redirect('login')

    unit = get_object_or_404(PalliativeUnit, user=request.user, is_verified=True)
    donation = get_object_or_404(
        MedicineDonation,
        id=donation_id,
        unit=unit,
        status='accepted'
    )

    if request.method == "POST":
        donation.status = 'collected'
        donation.save()

    return redirect('unit_donations')


# ==========================================
# UNIT LOGOUT
# ==========================================

def unit_logout(request):

    logout(request)

    return redirect('login')
