from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required 
from django.contrib.auth import get_user_model
from unit.models import PalliativeUnit
from user.models import MedicineDonation
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
        '03-admin/dashboard.html',
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

    unit = get_object_or_404(
        PalliativeUnit,
        id=unit_id
    )

    unit.is_verified = True
    unit.save()

    return redirect('admin_dashboard')



# ==========================================
# REJECT UNIT
# ==========================================
@login_required
def reject_unit(request, unit_id):

    if request.user.role != 'admin':
        return redirect('welcome')

    unit = get_object_or_404(
        PalliativeUnit,
        id=unit_id
    )

    user = unit.user
    user.delete()

    return redirect('admin_dashboard')


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
