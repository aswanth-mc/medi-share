from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required 
from django.contrib.auth import get_user_model
from django.contrib import messages
from unit.models import PalliativeUnit
from user.models import MedicineDonation, MedicineRequest
# Create your views here.

User = get_user_model()


# ==========================================
# DASHBOARD
# ==========================================

@login_required
def admin_dashboard(request):
    if request.user.role != 'admin':
        return redirect('welcome')
    
    pending_units = PalliativeUnit.objects.filter(is_verified=False)
    verified_units = PalliativeUnit.objects.filter(is_verified=True).count()
    total_units = pending_units.count() + verified_units
    total_users = User.objects.filter(role='user').count()
    total_donations = MedicineDonation.objects.exclude(status='removed').count()
    recent_donations = MedicineDonation.objects.exclude(status='removed')[:5]

    return render(
        request,
        '03-admin/admin_dashboard.html',
        {
            'pending_units': pending_units,
            'pending_count': pending_units.count(),
            'verified_units': verified_units,
            'total_units': total_units,
            'total_users': total_users,
            'total_donations': total_donations,
            'recent_donations': recent_donations,
        }
    )




# ==========================================
# APPROVE UNIT
# ==========================================
@login_required
def approve_unit(request, unit_id):

    if request.user.role != 'admin':
        return redirect('welcome')

    unit = get_object_or_404(PalliativeUnit, id=unit_id, is_verified=False)

    if request.method == 'POST':
        unit.is_verified = True
        unit.save()
        messages.success(request, f'{unit.name} has been verified!')
        return redirect('admin_dashboard')

    return render(request, '03-admin/approve_unit.html', {'unit': unit})


# ==========================================
# REJECT UNIT
# ==========================================

@login_required
def reject_unit(request, unit_id):

    if request.user.role != 'admin':
        return redirect('welcome')

    unit = get_object_or_404(PalliativeUnit, id=unit_id, is_verified=False)

    if request.method == 'POST':
        reason = request.POST.get('reason', 'No reason provided')
        unit.user.delete()
        messages.success(request, f'Unit {unit.name} has been rejected!')
        return redirect('admin_dashboard')

    return render(request, '03-admin/reject_unit.html', {'unit': unit})


# ==========================================
# ADMIN PROFILE
# ==========================================

@login_required
def admin_profile(request):
    """Display admin profile information"""
    if request.user.role != 'admin':
        return redirect('welcome')
    
    # Get platform statistics
    total_users = User.objects.filter(role='user').count()
    total_units = PalliativeUnit.objects.count()
    total_donations = MedicineDonation.objects.exclude(status='removed').count()
    total_requests = MedicineRequest.objects.count()
    verified_units = PalliativeUnit.objects.filter(is_verified=True).count()
    pending_units = PalliativeUnit.objects.filter(is_verified=False).count()
    
    context = {
        'user': request.user,
        'total_users': total_users,
        'total_units': total_units,
        'total_donations': total_donations,
        'total_requests': total_requests,
        'verified_units': verified_units,
        'pending_units': pending_units,
        'joined_date': request.user.created_at,
    }
    
    return render(request, '03-admin/profile.html', context)


@login_required
def admin_edit_profile(request):
    """Edit admin profile information"""
    if request.user.role != 'admin':
        return redirect('welcome')
    
    from .forms import AdminProfileEditForm
    
    if request.method == 'POST':
        form = AdminProfileEditForm(
            request.POST,
            instance=request.user,
            user=request.user
        )
        if form.is_valid():
            form.save()
            messages.success(request, 'Profile updated successfully!')
            return redirect('admin_profile')
        else:
            for field, errors in form.errors.items():
                for error in errors:
                    messages.error(request, f'{field}: {error}')
    else:
        form = AdminProfileEditForm(instance=request.user, user=request.user)
    
    context = {
        'form': form,
        'user': request.user,
    }
    
    return render(request, '03-admin/edit_profile.html', context)


@login_required
def admin_change_password(request):
    """Change admin password"""
    if request.user.role != 'admin':
        return redirect('welcome')
    
    from .forms import CurrentPasswordForm, PasswordChangeForm
    
    if request.method == 'POST':
        current_form = CurrentPasswordForm(request.user, request.POST)
        password_form = PasswordChangeForm(request.user, request.POST)
        
        if current_form.is_valid() and password_form.is_valid():
            user = password_form.save()
            messages.success(request, 'Password changed successfully!')
            return redirect('admin_profile')
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
    
    return render(request, '03-admin/edit_profile.html', context)


# ==========================================
# ADMIN DONATIONS
# ==========================================

@login_required
def admin_donations(request):

    if request.user.role != 'admin':
        return redirect('welcome')

    donations = MedicineDonation.objects.all()

    return render(
        request,
        '03-admin/admin_donations.html',
        {
            'donations': donations,
        }
    )


# ==========================================
# REMOVE DONATION
# ==========================================

@login_required
def remove_donation(request, donation_id):

    if request.user.role != 'admin':
        return redirect('welcome')

    donation = get_object_or_404(MedicineDonation, id=donation_id)

    if request.method == "POST":
        donation.status = 'removed'
        donation.save()

    return redirect('admin_donations')


# ==========================================
# UNITS PAGE
# ==========================================
@login_required
def units_page(request):

    units = PalliativeUnit.objects.all().order_by('-created_at')

    total_units = units.count()

    verified_units = units.filter(
        is_verified=True
    ).count()

    pending_units = units.filter(
        is_verified=False
    ).count()

    return render(
        request,
        '03-admin/units.html',
        {
            'units': units,
            'total_units': total_units,
            'verified_units': verified_units,
            'pending_units': pending_units,
        }
    )

@login_required
def admin_donations(request):


    if request.user.role != 'admin':
        return redirect('login')

    donations = (
        MedicineDonation.objects
        .select_related('donor', 'unit')
        .order_by('-created_at')
    )

    search_query = request.GET.get('q')

    if search_query:

        donations = donations.filter(
            medicine_name__icontains=search_query
        )
    

    return render(
        request,
        '03-admin/donations.html',
        {
            'donations': donations,
            'search_query': search_query,
        }
    )

@login_required
def admin_requests(request):


    if request.user.role != 'admin':
        return redirect('login')

    requests = (
        MedicineRequest.objects
        .select_related(
            'requester',
            'donation',
            'unit'
        )
        .order_by('-created_at')
)

    return render(
        request,
        '03-admin/requests.html',
        {
            'requests': requests
        }
    )



@login_required
def inventory_overview(request):


    if request.user.role != 'admin':
        return redirect('login')

    inventory = (
        MedicineDonation.objects
        .filter(status='collected')
        .select_related('unit')
        .order_by('expiry_date')
    )

    return render(
        request,
        '03-admin/inventory_overview.html',
        {
            'inventory': inventory
        }
    )





