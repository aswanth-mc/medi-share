from django.shortcuts import render, redirect 
from django.contrib.auth.decorators import login_required 
from django.contrib.auth import get_user_model
from unit .models import PalliativeUnit
# Create your views here.

User = get_user_model()

@login_required
def admin_dashboard(request):
    if request.user.role != 'admin':
        return redirect('login')
    pending_units = User.objects.filter(role='unit', verification_status='pending')
    context = {'pending_units': pending_units}
    return render(request, 'admin_dashboard.html', context)

@login_required
def approve_unit(request, unit_id):
    if request.user.role != 'admin':
        return redirect('login')

    try:
        unit = User.objects.get(id=unit_id, role='unit')
        unit.verification_status = 'approved'
        unit.save()
    except User.DoesNotExist:
        pass

    return redirect('admin_dashboard')

@login_required
def reject_unit(request, unit_id):
    if request.user.role != 'admin':
        return redirect('login')

    try:
        unit = User.objects.get(id=unit_id, role='unit')
        unit.verification_status = 'rejected'
        unit.save()
    except User.DoesNotExist:
        pass

    return redirect('admin_dashboard')