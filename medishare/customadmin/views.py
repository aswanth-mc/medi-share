from django.contrib.auth import get_user_model
from django.db.models import Count, Sum
from django.utils.timezone import now
from datetime import timedelta

from unit.models import PalliativeUnit
from user.models import MedicineDonation, MedicineRequest

User = get_user_model()
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required


# ==========================================
# DASHBOARD
# ==========================================

@login_required
def admin_dashboard(request):

    if request.user.role != 'admin':
        return redirect('welcome')

    # =========================
    # COUNTS
    # =========================

    total_users = User.objects.filter(role='user').count()

    total_units = PalliativeUnit.objects.count()

    verified_units = PalliativeUnit.objects.filter(
        is_verified=True
    ).count()

    pending_count = PalliativeUnit.objects.filter(
        is_verified=False
    ).count()

    total_donations = MedicineDonation.objects.count()

    total_requests = MedicineRequest.objects.count()

    inventory_count = MedicineDonation.objects.filter(
        status='collected'
    ).aggregate(
        total=Sum('quantity')
    )['total'] or 0

    # =========================
    # PENDING UNITS
    # =========================

    pending_units = PalliativeUnit.objects.filter(
        is_verified=False
    ).order_by('-created_at')

    # =========================
    # RECENT DONATIONS
    # =========================

    recent_donations = MedicineDonation.objects.select_related(
        'donor',
        'unit'
    ).order_by('-created_at')[:5]

    # =========================
    # REQUEST STATS
    # =========================

    completed_requests = MedicineRequest.objects.filter(
        status='fulfilled'
    ).count()

    pending_requests = MedicineRequest.objects.filter(
        status='pending'
    ).count()

    urgent_requests = MedicineRequest.objects.filter(
        quantity__gte=5
    ).count()

    # =========================
    # LOW STOCK ITEMS
    # =========================

    low_stock_items = MedicineDonation.objects.filter(
        status='collected',
        quantity__lte=5
    ).count()

    # =========================
    # EXPIRED ITEMS
    # =========================

    expired_items = MedicineDonation.objects.filter(
        expiry_date__lt=now().date()
    ).count()

    # =========================
    # RECENT ACTIVITY
    # =========================

    recent_activity = []

    latest_units = PalliativeUnit.objects.order_by(
        '-created_at'
    )[:2]

    for unit in latest_units:
        recent_activity.append({
            'icon': 'hospital',
            'title': f'{unit.name} registered',
            'time': unit.created_at,
        })

    latest_donations = MedicineDonation.objects.order_by(
        '-created_at'
    )[:2]

    for donation in latest_donations:
        recent_activity.append({
            'icon': 'capsule',
            'title': f'{donation.medicine_name} donated',
            'time': donation.created_at,
        })

    latest_requests = MedicineRequest.objects.order_by(
        '-created_at'
    )[:2]

    for req in latest_requests:
        recent_activity.append({
            'icon': 'clipboard2-pulse',
            'title': f'Request for {req.donation.medicine_name}',
            'time': req.created_at,
        })

    recent_activity = sorted(
        recent_activity,
        key=lambda x: x['time'],
        reverse=True
    )[:6]

    context = {

        'total_users': total_users,
        'total_units': total_units,
        'verified_units': verified_units,
        'pending_count': pending_count,
        'total_donations': total_donations,
        'total_requests': total_requests,
        'inventory_count': inventory_count,
        'pending_units': pending_units,
        'recent_donations': recent_donations,
        'completed_requests': completed_requests,
        'pending_requests': pending_requests,
        'low_stock_items': low_stock_items,
        'expired_items': expired_items,
        'recent_activity': recent_activity,
    }

    return render(
        request,
        '03-admin/admin_dashboard.html',
        context
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
        '03-admin/edit_profile.html',
        context
    )


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





