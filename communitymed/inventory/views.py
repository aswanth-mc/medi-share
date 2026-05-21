from django.shortcuts import redirect, render
from django.contrib.auth.decorators import login_required
from inventory.models import MedicineDonation, UnitInventory


@login_required
def collect_donation(request, donation_id):

    if request.user.role != 'unit':
        return redirect('home')

    donation = MedicineDonation.objects.get(id=donation_id)

    # change donation status
    donation.status = 'collected'
    donation.save()

    # move to inventory
    UnitInventory.objects.create(
        unit=request.user,
        donation=donation,
        medicine_name=donation.medicine_name,
        quantity=donation.quantity,
        category=donation.category,
        expiry_date=donation.expiry_date
    )

    return redirect('unit_inventory')

@login_required
def unit_inventory(request):

    if request.user.role != 'unit':
        return redirect('home')

    inventory_items = UnitInventory.objects.filter(
        unit=request.user
    ).order_by('-added_at')

    context = {
        'inventory_items': inventory_items
    }

    return render(
        request,
        'unit/inventory.html',
        context
    )