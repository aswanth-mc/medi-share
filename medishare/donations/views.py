from urllib import request

from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required

from donations.models import Donation
from donations.utils import calculate_distance

from unit.models import PalliativeUnit
# Create your views here.


@login_required
def create_donation(request):

    if request.method == "POST":

        medicine_name = request.POST.get('medicine_name')
        quantity = request.POST.get('quantity')
        expiry_date = request.POST.get('expiry_date')
        description = request.POST.get('description')
        latitude = request.POST.get('latitude')
        longitude = request.POST.get('longitude')
        medicine_image = request.FILES.get('medicine_image')

        nearest_unit = PalliativeUnit.objects.filter(
            is_verified=True
        ).first()

        Donation.objects.create(
            donor=request.user,
            unit=nearest_unit,
            medicine_name=medicine_name,
            quantity=quantity,
            expiry_date=expiry_date,
            medicine_image=medicine_image,
            description=description,
            latitude=latitude,
            longitude=longitude,
            status='pending'
        )

        return redirect('user_dashboard')

    return render(request, '05-user/create_donation.html')

@login_required
def incoming_donations(request):

    unit = PalliativeUnit.objects.get(user=request.user)

    donations = Donation.objects.filter(
        unit=unit
    ).exclude(status='received')

    return render(
        request,
        '04-unit/incoming_donations.html',
        {
            'donations': donations
        }
    )

@login_required
def accept_donation(request, donation_id):

    donation = Donation.objects.get(id=donation_id)

    donation.status = 'accepted'

    donation.save()

    return redirect('incoming_donations')

@login_required
def collect_donation(request, donation_id):

    donation = Donation.objects.get(id=donation_id)

    donation.status = 'collected'

    donation.save()

    return redirect('incoming_donations')