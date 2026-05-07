from django.shortcuts import redirect, render
from django.contrib.auth.decorators import login_required
from inventory.models import MedicineDonation, UnitInventory

# Create your views here.
@login_required
def collect_donation(request, donation_id):
    if request.user.role != 'unit':
        return redirect('home')

    donation = MedicineDonation.objects.get(id=donation_id)

    donation.status = 'collected'
    donation.save()

    UnitInventory.objects.create(
        unit=request.user,
        donation=donation,
        name=donation.name,
        quantity=donation.quantity,
        category=donation.category,
        expiry_date=donation.expiry_date
    )

    return redirect('unit_dashboard')