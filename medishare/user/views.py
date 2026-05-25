
from pyexpat.errors import messages
from urllib import request

from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404
from django.db.models import Count, F, Q, Sum
from django.utils import timezone
from django.contrib import messages

from .utils.geo import find_nearest_unit

from .models import MedicineDonation, MedicineRequest
from .forms import UserProfileEditForm

User = get_user_model()


# ==========================================
# WELCOME PAGE
# ==========================================

def welcome_view(request):
    return render(request, '01-welcome/welcome.html')


# ==========================================
# REGISTER CHOICE PAGE
# ==========================================

def register_choice(request):
    return render(request, '02-auth/register_choice.html')


# ==========================================
# USER REGISTER
# ==========================================

def register_user(request):

    if request.method == "POST":

        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')
        phone = request.POST.get('phone')

        location_name = request.POST.get('location_name')
        latitude = request.POST.get('latitude')
        longitude = request.POST.get('longitude')

        # CHECK EMAIL EXISTS
        if User.objects.filter(email=email).exists():

            return render(
                request,
                '05-user/registration.html',
                {
                    'error': 'Email already exists'
                }
            )

        # CREATE USER
        user = User.objects.create_user(
            username=username,
            email=email,
            password=password,
            role='user',
            phone=phone,
            location_name=location_name,
            latitude=latitude,
            longitude=longitude
        )

        return redirect('login')

    return render(request, '05-user/registration.html')


# ==========================================
# USER LOGIN
# ==========================================

def user_login(request):

    if request.method == "POST":

        email = request.POST.get('email')
        password = request.POST.get('password')

        try:
            user_obj = User.objects.get(email=email)

        except User.DoesNotExist:

            return render(
                request,
                '02-auth/login.html',
                {
                    'error': 'Invalid email or password'
                }
            )

        user = authenticate(
            request,
            username=user_obj.username,
            password=password
        )

        if user is not None:

            login(request, user)

            # ROLE BASED REDIRECT
            if user.role == 'admin':
                return redirect('admin_dashboard')

            elif user.role == 'unit':
                return redirect('unit_dashboard')

            else:
                return redirect('user_dashboard')

        return render(
            request,
            '02-auth/login.html',
            {
                'error': 'Invalid email or password'
            }
        )

    return render(request, '02-auth/login.html')


# ==========================================
# USER DASHBOARD
# ==========================================

@login_required
def user_dashboard(request):

    if request.user.role != 'user':
        return redirect('login')

    donations = MedicineDonation.objects.filter(donor=request.user)

    available_medicines = (
        MedicineDonation.objects
        .filter(
            status='collected',
            unit__isnull=False,
            unit__is_verified=True,
            quantity__gt=0,
        )
        .select_related('unit')
        .exclude(expiry_date__lt=timezone.now().date())
        .annotate(
            reserved=Count(
                'medicine_requests',
                filter=Q(medicine_requests__status__in=['pending', 'approved']),
            )
        )
        .filter(quantity__gt=F('reserved'))
    )

    search_query = request.GET.get('q', '').strip()
    if search_query:
        available_medicines = available_medicines.filter(
            medicine_name__icontains=search_query
        )

    return render(
        request,
        '05-user/dashboard.html',
        {
            'donations': donations,
            'available_medicines': available_medicines,
            'search_query': search_query,
        }
    )


# ==========================================
# REQUEST MEDICINE FROM UNIT INVENTORY
# ==========================================

@login_required
def request_medicine(request, donation_id):

    if request.user.role != 'user':
        return redirect('login')

    if request.method != 'POST':
        return redirect('user_dashboard')

    donation = get_object_or_404(
        MedicineDonation,
        id=donation_id,
        status='collected',
        unit__isnull=False,
        unit__is_verified=True,
    )

    requested_quantity = request.POST.get('quantity')

    # EMPTY CHECK
    if not requested_quantity:

        messages.error(
            request,
            'Please enter quantity.'
        )

        return redirect('user_dashboard')

    # INTEGER CHECK
    try:

        requested_quantity = int(requested_quantity)

    except ValueError:

        messages.error(
            request,
            'Invalid quantity.'
        )

        return redirect('user_dashboard')

    # NEGATIVE CHECK
    if requested_quantity < 1:

        messages.error(
            request,
            'Quantity must be at least 1.'
        )

        return redirect('user_dashboard')

    # EXPIRED MEDICINE
    if donation.expiry_date < timezone.now().date():

        messages.error(
            request,
            'This medicine has expired.'
        )

        return redirect('user_dashboard')

    # AVAILABLE STOCK
    approved_reserved = (
        MedicineRequest.objects.filter(
            donation=donation,
            status__in=['pending', 'approved']
        )
        .aggregate(total=Sum('quantity'))['total']
        or 0
    )

    available_stock = donation.quantity - approved_reserved

    if requested_quantity > available_stock:

        messages.error(
            request,
            f'Only {available_stock} medicines available.'
        )

        return redirect('user_dashboard')

    # EXISTING REQUEST
    if MedicineRequest.objects.filter(
        requester=request.user,
        donation=donation,
        status__in=['pending', 'approved'],
    ).exists():

        messages.error(
            request,
            'You already requested this medicine.'
        )

        return redirect('request_status')

    # CREATE REQUEST
    MedicineRequest.objects.create(
        requester=request.user,
        donation=donation,
        unit=donation.unit,
        quantity=requested_quantity,
    )

    messages.success(
        request,
        f'Request sent for {requested_quantity} quantity of {donation.medicine_name}.'
    )

    return redirect('request_status')

# ==========================================
# REQUEST STATUS
# ==========================================

@login_required
def request_status(request):

    if request.user.role != 'user':
        return redirect('login')

    medicine_requests = (
        MedicineRequest.objects
        .filter(requester=request.user)
        .select_related('donation', 'unit')
    )

    return render(
        request,
        '05-user/request_status.html',
        {
            'medicine_requests': medicine_requests,
        }
    )


# ==========================================
# DONATE MEDICINE
# ==========================================

@login_required
def donate_medicine(request):

    if request.user.role != 'user':
        return redirect('login')

    if request.method == "POST":
        medicine_name = request.POST.get('medicine_name')
        expiry_date = request.POST.get('expiry_date')
        quantity = request.POST.get('quantity')
        pickup_location = request.POST.get('pickup_location')
        latitude = request.POST.get('latitude')
        longitude = request.POST.get('longitude')
        medicine_image = request.FILES.get('medicine_image')

        if not medicine_name:
            return render(request, '05-user/donate_medicine.html', {'error': 'Medicine name is required'})

        if not expiry_date:
            return render(request, '05-user/donate_medicine.html', {'error': 'Expiry date is required'})

        if not quantity:
            return render(request, '05-user/donate_medicine.html', {'error': 'Quantity is required'})

        if not medicine_image:
            return render(request, '05-user/donate_medicine.html', {'error': 'Medicine image is required'})

        if not latitude or not longitude:
            return render(
                request,
                '05-user/donate_medicine.html',
                {'error': 'Please select a pickup location on the map.'},
            )

        nearest_unit, _ = find_nearest_unit(latitude, longitude)
        if not nearest_unit:
            return render(
                request,
                '05-user/donate_medicine.html',
                {
                    'error': (
                        'No verified unit is available near this location. '
                        'Try another pickup point or try again later.'
                    ),
                },
            )

        MedicineDonation.objects.create(
            donor=request.user,
            unit=nearest_unit,
            medicine_name=medicine_name,
            medicine_image=medicine_image,
            expiry_date=expiry_date,
            quantity=quantity,
            pickup_location=pickup_location,
            latitude=latitude,
            longitude=longitude,
        )

        return redirect('user_dashboard')

    return render(request, '05-user/donate_medicine.html')


# ==========================================
# VIEW DONATION
# ==========================================

@login_required
def my_donations(request):

    donations = (
        MedicineDonation.objects
        .filter(donor=request.user)
        .select_related('unit')
        .order_by('-created_at')
    )

    return render(
        request,
        '05-user/my_donations.html',
        {
            'donations': donations
        }
    )


# ==========================================

# CANCEL DONATION

# ==========================================

@login_required
def cancel_donation(request, donation_id):


    if request.user.role != 'user':
        return redirect('login')

    donation = get_object_or_404(
        MedicineDonation,
        id=donation_id,
        donor=request.user,
        status='pending'
    )

    if request.method == "POST":

        donation.status = 'cancelled'
        donation.save()

        messages.success(
            request,
            'Donation cancelled successfully.'
        )

    return redirect('my_donations')


# ==========================================
# USER PROFILE
# ==========================================

@login_required
def user_profile(request):
    """Display user profile information"""
    if request.user.role != 'user':
        return redirect('login')
    
    # Get user statistics
    total_donations = MedicineDonation.objects.filter(donor=request.user).count()
    total_requests = MedicineRequest.objects.filter(requester=request.user).count()
    active_requests = MedicineRequest.objects.filter(
        requester=request.user,
        status__in=['pending', 'approved']
    ).count()
    
    context = {
        'user': request.user,
        'total_donations': total_donations,
        'total_requests': total_requests,
        'active_requests': active_requests,
        'joined_date': request.user.created_at,
    }
    
    return render(request, '05-user/profile.html', context)


@login_required
def user_edit_profile(request):
    """Edit user profile information"""
    if request.user.role != 'user':
        return redirect('login')
    
    from .forms import UserProfileEditForm
    
    if request.method == 'POST':
        form = UserProfileEditForm(
            request.POST,
            instance=request.user,
            user=request.user
        )
        if form.is_valid():
            form.save()
            messages.success(request, 'Profile updated successfully!')
            return redirect('user_profile')
        else:
            for field, errors in form.errors.items():
                for error in errors:
                    messages.error(request, f'{field}: {error}')
    else:
        form = UserProfileEditForm(instance=request.user, user=request.user)
    
    context = {
        'form': form,
        'user': request.user,
    }
    
    return render(request, '05-user/edit_profile.html', context)



@login_required
def user_change_password(request):
    """Change user password"""
    if request.user.role != 'user':
        return redirect('login')
    
    from .forms import CurrentPasswordForm, PasswordChangeForm
    
    if request.method == 'POST':
        current_form = CurrentPasswordForm(request.user, request.POST)
        password_form = PasswordChangeForm(request.user, request.POST)
        
        if current_form.is_valid() and password_form.is_valid():
            user = password_form.save()
            messages.success(request, 'Password changed successfully!')
            return redirect('user_profile')
        else:
            if current_form.errors:
                for error in current_form.errors.get('current_password', []):
                    messages.error(request, error)
            if password_form.errors:
                for field, errors in password_form.errors.items():
                    for error in errors:
                        messages.error(request, f'{field}: {error}')
    else:
        current_form = CurrentPasswordForm(request.user)
        password_form = PasswordChangeForm(request.user)
    
    context = {
        'current_form': current_form,
        'password_form': password_form,
        'user': request.user,
    }
    
    return render(request, '05-user/edit_profile.html', context)

# ==========================================
# LOGOUT
# ==========================================

def user_logout(request):

    logout(request)

    return redirect('login')



