from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required 
from django.contrib.auth import get_user_model
from unit .models import PalliativeUnit
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

    return render(request, 'admin_dashboard.html', {'pending_units': pending_units})




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