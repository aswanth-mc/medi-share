from django.shortcuts import render, redirect

from django.contrib.auth.decorators import login_required

from donations.models import Donation
from inventory.models import Inventory
# Create your views here.



@login_required
def receive_donation(request, donation_id):

    donation = Donation.objects.get(id=donation_id)

    Inventory.objects.create(
        unit=donation.unit,
        medicine_name=donation.medicine_name,
        quantity=donation.quantity,
        expiry_date=donation.expiry_date,
        medicine_image=donation.medicine_image,
        description=donation.description
    )

    donation.status = 'received'

    donation.save()

    return redirect('incoming_donations')