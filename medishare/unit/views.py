from django.contrib.auth import login, logout
from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db import transaction
import json
from django.shortcuts import get_object_or_404, render, redirect
from .models import PalliativeUnit
from user.models import MedicineDonation, MedicineRequest

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

    
    if not unit.is_verified:
        return redirect('verification_pending')

    total_donations = MedicineDonation.objects.filter( unit=unit ).count()
    pending_donations = MedicineDonation.objects.filter(status='pending', unit=unit)[:5]
    accepted_donations = MedicineDonation.objects.filter(unit=unit, status='accepted')
    collected_donations = MedicineDonation.objects.filter(unit=unit, status='collected')
    pending_requests_count = MedicineRequest.objects.filter(unit=unit,status='pending').count()
    inventory_stock = collected_donations.count()
    pending_requests_count = MedicineRequest.objects.filter(unit=unit,status='pending').count()
    approved_requests_count = MedicineRequest.objects.filter( unit=unit, status='approved' ).count()
    fulfilled_requests_count = MedicineRequest.objects.filter( unit=unit, status='fulfilled' ).count()

    recent_requests = ( MedicineRequest.objects .filter(unit=unit) .select_related('requester', 'donation') .order_by('-created_at')[:5] )
    inventory_preview = ( MedicineDonation.objects .filter( unit=unit, status='collected' ) .order_by('-created_at')[:6] )

    # monthly donations
    from django.db.models.functions import ExtractMonth 
    from django.db.models import Count 
    import json

    monthly_data = ( MedicineDonation.objects .filter(unit=unit) .annotate(month=ExtractMonth('created_at')) .values('month') .annotate(total=Count('id')) .order_by('month') )
    month_labels=[]
    month_totals=[]
    month_names = [ 'Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec' ]    
    for item in monthly_data: 
        month_labels.append( month_names[item['month']-1] ) 
        month_totals.append( item['total'] )

# INVENTORY HEALTH

    total_inventory = (
    MedicineDonation.objects
        .filter(
            unit=unit,
            status='collected'
        )
        .count()
        )

    healthy_inventory = (
        MedicineDonation.objects
            .filter(
                unit=unit,
                status='collected',
                quantity__gt=0
            )
            .count()
)

    if total_inventory > 0:

        inventory_health = int(
            (healthy_inventory / total_inventory) * 100
        )

    else:

        inventory_health = 0


    dash_offset = 377 - (
        (inventory_health / 100) * 377
    )

    return render(
    request,
    '04-unit/dashboard.html',
    {
        'unit': unit,

        'total_donations':
            accepted_donations.count()
            + collected_donations.count(),

        'pending_donations':
            pending_donations.count(),

        'inventory_stock':
            inventory_stock,

        'pending_requests_count':
            pending_requests_count,

        'recent_requests':
            recent_requests,

        'inventory_preview':
            inventory_preview,

        'chart_labels':
            json.dumps(month_labels),

        'chart_data':
            json.dumps(month_totals),

        'inventory_health':
            inventory_health,

        'dash_offset':
            dash_offset,
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
# UNIT MEDICINE REQUESTS
# ==========================================

@login_required
def unit_requests(request):

    if request.user.role != 'unit':
        return redirect('login')

    unit = get_object_or_404(PalliativeUnit, user=request.user)

    if not unit.is_verified:
        return redirect('verification_pending')

    all_requests = (
        MedicineRequest.objects
        .filter(unit=unit)
        .select_related('requester', 'donation')
    )

    return render(
        request,
        '04-unit/unit_request.html',
        {
            'unit': unit,
            'pending_requests': all_requests.filter(status='pending'),
            'approved_requests': all_requests.filter(status='approved'),
            'rejected_requests': all_requests.filter(status='rejected'),
            'fulfilled_requests': all_requests.filter(status='fulfilled'),
        }
    )


@login_required
def approve_request(request, request_id):

    if request.user.role != 'unit':
        return redirect('login')

    unit = get_object_or_404(PalliativeUnit, user=request.user, is_verified=True)
    medicine_request = get_object_or_404(
        MedicineRequest,
        id=request_id,
        unit=unit,
        status='pending',
    )

    if request.method == 'POST':
        medicine_request.status = 'approved'
        medicine_request.save()
        messages.success(
            request,
            f'Approved request for {medicine_request.donation.medicine_name}.',
        )

    return redirect('unit_requests')


@login_required
def reject_request(request, request_id):

    if request.user.role != 'unit':
        return redirect('login')

    unit = get_object_or_404(PalliativeUnit, user=request.user, is_verified=True)
    medicine_request = get_object_or_404(
        MedicineRequest,
        id=request_id,
        unit=unit,
        status='pending',
    )

    if request.method == 'POST':
        medicine_request.status = 'rejected'
        medicine_request.save()
        messages.success(
            request,
            f'Rejected request for {medicine_request.donation.medicine_name}.',
        )

    return redirect('unit_requests')


@login_required
def collect_request(request, request_id):

    if request.user.role != 'unit':
        return redirect('login')

    unit = get_object_or_404(PalliativeUnit, user=request.user, is_verified=True)
    medicine_request = get_object_or_404(
        MedicineRequest,
        id=request_id,
        unit=unit,
        status='approved',
    )

    if request.method != 'POST':
        return redirect('unit_requests')

    with transaction.atomic():
        donation = MedicineDonation.objects.select_for_update().get(
            pk=medicine_request.donation_id
        )

        if donation.quantity < medicine_request.quantity:
            messages.error(request, 'This medicine is no longer in stock.')
            return redirect('unit_requests')

        medicine_request.status = 'fulfilled'
        medicine_request.save()

        donation.quantity -= medicine_request.quantity
        donation.save()

    messages.success(
        request,
        f'Marked {medicine_request.donation.medicine_name} as collected for {medicine_request.requester.username}.',
    )
    return redirect('unit_requests')


# ==========================================
# INVENTORY DASHBOARD
# ==========================================

@login_required
def inventory_dashboard(request):

    # ONLY UNIT ACCESS
    if request.user.role != 'unit':
        return redirect('login')

    try:
        unit = PalliativeUnit.objects.get(
            user=request.user
        )

    except PalliativeUnit.DoesNotExist:

        return redirect('login')

    # CHECK VERIFIED
    if not unit.is_verified:

        return redirect('verification_pending')

    # INVENTORY ITEMS
    inventory_items = MedicineDonation.objects.filter(
        unit=unit,
        status='collected'
    ).order_by('-created_at')

    return render(
        request,
        '04-unit/inventory_dashboard.html',
        {
            'inventory_items': inventory_items,
            'unit': unit
        }
    )

# ==========================================
# EDIT INVENTORY ITEM
# ==========================================

@login_required
def edit_inventory_item(request, donation_id):

    if request.user.role != 'unit':
        return redirect('login')

    unit = get_object_or_404(
        PalliativeUnit,
        user=request.user,
        is_verified=True
    )

    item = get_object_or_404(
        MedicineDonation,
        id=donation_id,
        unit=unit,
        status='collected'
    )

    if request.method == "POST":

        item.medicine_name = request.POST.get(
            'medicine_name'
        )

        item.quantity = request.POST.get(
            'quantity'
        )

        item.expiry_date = request.POST.get(
            'expiry_date'
        )

        item.description = request.POST.get(
            'description'
        )

        # OPTIONAL IMAGE UPDATE
        if request.FILES.get('medicine_image'):
            item.medicine_image = request.FILES.get(
                'medicine_image'
            )

        item.save()

        return redirect('inventory_dashboard')

    return render(
        request,
        '04-unit/edit_inventory_item.html',
        {
            'item': item
        }
    )

# ==========================================
# DELETE INVENTORY ITEM
# ==========================================

@login_required
def delete_inventory_item(request, donation_id):

    if request.user.role != 'unit':
        return redirect('login')

    unit = get_object_or_404(
        PalliativeUnit,
        user=request.user,
        is_verified=True
    )

    item = get_object_or_404(
        MedicineDonation,
        id=donation_id,
        unit=unit,
        status='collected'
    )

    item.delete()

    return redirect('inventory_dashboard')


# ==========================================
# UNIT PROFILE
# ==========================================

@login_required
def unit_profile(request):
    """Display unit profile information"""
    if request.user.role != 'unit':
        return redirect('login')
    
    try:
        unit = PalliativeUnit.objects.get(user=request.user)
    except PalliativeUnit.DoesNotExist:
        return redirect('login')
    
    # Get unit statistics
    total_donations = MedicineDonation.objects.filter(unit=unit).exclude(status='removed').count()
    inventory_count = MedicineDonation.objects.filter(unit=unit, status='collected').count()
    pending_requests = MedicineRequest.objects.filter(unit=unit, status='pending').count()
    
    context = {
        'unit': unit,
        'user': request.user,
        'total_donations': total_donations,
        'inventory_count': inventory_count,
        'pending_requests': pending_requests,
        'joined_date': unit.created_at,
    }
    
    return render(request, '04-unit/profile.html', context)


@login_required
def unit_edit_profile(request):
    """Edit unit profile information"""
    if request.user.role != 'unit':
        return redirect('login')
    
    try:
        unit = PalliativeUnit.objects.get(user=request.user)
    except PalliativeUnit.DoesNotExist:
        return redirect('login')
    
    from .forms import UnitProfileEditForm
    
    if request.method == 'POST':
        form = UnitProfileEditForm(request.POST, user=request.user)
        if form.is_valid():
            unit.name = form.cleaned_data.get('name')
            unit.email = form.cleaned_data.get('email')
            unit.phone = form.cleaned_data.get('phone')
            unit.location_name = form.cleaned_data.get('location_name')
            unit.save()
            
            # Also update the User email
            request.user.email = form.cleaned_data.get('email')
            request.user.save()
            
            messages.success(request, 'Profile updated successfully!')
            return redirect('unit_profile')
        else:
            for field, errors in form.errors.items():
                for error in errors:
                    messages.error(request, f'{field}: {error}')
    else:
        initial_data = {
            'name': unit.name,
            'email': unit.email,
            'phone': unit.phone,
            'location_name': unit.location_name,
        }
        form = UnitProfileEditForm(initial=initial_data, user=request.user)
    
    context = {
        'form': form,
        'unit': unit,
        'user': request.user,
    }
    
    return render(request, '04-unit/edit_profile.html', context)


from django.contrib.auth import update_session_auth_hash

@login_required
def admin_change_password(request):

    if request.user.role != 'admin':
        return redirect('welcome')

    from .forms import CurrentPasswordForm, PasswordChangeForm

    if request.method == 'POST':

        current_form = CurrentPasswordForm(
            request.user,
            request.POST
        )

        password_form = PasswordChangeForm(
            request.user,
            request.POST
        )

        if current_form.is_valid() and password_form.is_valid():

            user = password_form.save()

            # IMPORTANT
            update_session_auth_hash(
                request,
                user
            )

            messages.success(
                request,
                'Password changed successfully!'
            )

            return redirect('admin_profile')

        else:

            if current_form.errors:

                for error in current_form.errors.get(
                    'current_password',
                    []
                ):

                    messages.error(
                        request,
                        error
                    )

            if password_form.errors:

                for field, errors in password_form.errors.items():

                    for error in errors:

                        messages.error(
                            request,
                            f'{field}: {error}'
                        )

    else:

        current_form = CurrentPasswordForm(
            request.user
        )

        password_form = PasswordChangeForm(
            request.user
        )

    context = {

        'current_form': current_form,
        'password_form': password_form,
        'user': request.user,

    }

    return render(
        request,
        '04-unit/edit_profile.html',
        context
    )

# ==========================================
# UNIT LOGOUT
# ==========================================

def unit_logout(request):

    logout(request)

    return redirect('login')
